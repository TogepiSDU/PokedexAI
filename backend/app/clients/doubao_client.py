import json
from typing import Dict, Any, Optional
import httpx
from fastapi import HTTPException
from app.clients.http_client import HTTPClient
from app.core.config import settings


class DoubaoClient:
    """豆包 LLM 客户端"""
    
    def __init__(self):
        self.http_client = HTTPClient(
            base_url=settings.doubao_api_base_url,
            timeout=30  # LLM 请求可能需要更长时间
        )
        self.api_key = settings.doubao_api_key
    
    async def parse_question_to_intent(self, question: str) -> Dict[str, Any]:
        """将用户问题解析为结构化意图
        
        Args:
            question: 用户的自然语言问题
        
        Returns:
            包含意图信息的字典，格式如下：
            {
                "pokemon_name": "charizard",  # 宝可梦英文名
                "original_name": "喷火龙",     # 用户原始称呼
                "intent_type": "basic_info",   # 意图类型
                "detail_level": "normal"       # 详细程度
            }
        """
        system_prompt = """
你是宝可梦图鉴助手，负责解析用户关于宝可梦的问题，提取结构化意图。
请严格按照以下JSON格式输出，不要添加任何额外解释：
{"pokemon_name":"宝可梦英文名（小写）","original_name":"用户问题中提到的宝可梦名称","intent_type":"意图类型（如basic_info、stats、evolution、intro等）","detail_level":"详细程度（low/normal/high）"}
无法识别宝可梦名称时，将pokemon_name设为空字符串。
        """
        
        user_prompt = f"用户问题：{question}\n请只输出 JSON："
        
        try:
            response = await self.chat(system_prompt, user_prompt)
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"豆包返回的 JSON 格式无效: {str(e)}")
    
    async def build_answer_with_doubao(self, question: str, pokemon_data: Dict[str, Any], species_data: Dict[str, Any]) -> str:
        """根据宝可梦数据和用户问题生成自然语言回答
        
        Args:
            question: 用户的自然语言问题
            pokemon_data: 宝可梦详细数据（来自 /pokemon API）
            species_data: 宝可梦物种数据（来自 /pokemon-species API）
        
        Returns:
            生成的自然语言回答
        """
        # 精简宝可梦数据，只保留必要信息以减少token消耗
        simplified_pokemon = {
            "name": pokemon_data.get("name"),
            "height": pokemon_data.get("height"),
            "weight": pokemon_data.get("weight"),
            "types": [t["type"]["name"] for t in pokemon_data.get("types", [])],
            "stats": {s["stat"]["name"]: s["base_stat"] for s in pokemon_data.get("stats", [])},
            "abilities": [a["ability"]["name"] for a in pokemon_data.get("abilities", []) if not a["is_hidden"]],
            "hidden_ability": next((a["ability"]["name"] for a in pokemon_data.get("abilities", []) if a["is_hidden"]), None),
            "moves": [m["move"]["name"] for m in pokemon_data.get("moves", [])[:10]]  # 只保留前10个技能
        }
        
        # 精简物种数据
        simplified_species = {
            "name": species_data.get("name"),
            "capture_rate": species_data.get("capture_rate"),
            "base_happiness": species_data.get("base_happiness"),
            "growth_rate": species_data.get("growth_rate", {}).get("name"),
            "egg_groups": [g["name"] for g in species_data.get("egg_groups", [])],
            "color": species_data.get("color", {}).get("name"),
            "flavor_text": next((f["flavor_text"] for f in species_data.get("flavor_text_entries", []) if f["language"]["name"] == "zh-Hans"), "")
        }
        
        system_prompt = f"""
你是宝可梦专家，根据提供的数据用简洁中文回答用户问题。回答要求：
1. 先整体概括
2. 分点说明关键信息（属性、种族值、特性等）
3. 问题涉及进化时附上进化信息
4. 语言通俗易懂，不编造数据，严格基于提供信息
5. 控制在200字以内，言简意赅

用户问题：{question}

宝可梦数据：{json.dumps(simplified_pokemon, ensure_ascii=False)}
宝可梦物种数据：{json.dumps(simplified_species, ensure_ascii=False)}
        """
        
        user_prompt = "请根据以上信息回答用户的问题："
        
        try:
            return await self.chat(system_prompt, user_prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"豆包回答生成失败: {str(e)}")
    
    async def chat(self, system_prompt: str, user_prompt: str) -> str:
        """调用豆包 API 进行对话
        
        Args:
            system_prompt: 系统提示
            user_prompt: 用户提示
        
        Returns:
            豆包的回答
        """
        endpoint = "chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "doubao-seed-code-preview-251028",  # 根据新的豆包 API 配置更新模型
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,  # 控制回答的创意程度
            "max_completion_tokens": 1000,  # 降低生成的最大token数，足够回答宝可梦相关问题
            "top_p": 0.8  # 控制生成的多样性，减少不必要的token消耗
        }
        
        try:
            # 使用初始化时创建的 HTTPClient 实例
            result = await self.http_client.post(
                endpoint,
                headers=headers,
                data=payload
            )
            
            # 直接使用返回的字典结果
            return result["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            print(f"HTTP状态错误: {str(e)}")
            raise HTTPException(status_code=500, detail=f"豆包 API 请求失败: {str(e)} - 响应内容: {e.response.text if hasattr(e.response, 'text') else '无'}")
        except httpx.RequestError as e:
            print(f"请求错误: {str(e)}")
            raise HTTPException(status_code=503, detail=f"无法连接到豆包服务器: {str(e)}")
        except KeyError as e:
            print(f"KeyError: {str(e)}")
            raise HTTPException(status_code=500, detail=f"豆包 API 返回格式错误: 缺少 {str(e)} 字段")