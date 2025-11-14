import asyncio
import json
from app.clients.doubao_client import DoubaoClient
from app.core.config import settings

async def test_token_consumption():
    """测试优化后的token消耗情况"""
    print("=== 测试优化后的token消耗 ===")
    
    # 初始化豆包客户端
    doubao_client = DoubaoClient()
    
    # 测试意图解析的token消耗
    print("\n1. 测试意图解析:")
    user_question = "皮卡丘的特性是什么？"
    
    try:
        # 调用意图解析
        intent_result = await doubao_client.parse_question_to_intent(user_question)
        print(f"意图解析结果: {json.dumps(intent_result, ensure_ascii=False, indent=2)}")
        
        # 模拟宝可梦数据
        mock_pokemon = {
            "id": 25,
            "name": "皮卡丘",
            "types": ["电"],
            "base_experience": 112,
            "height": 4,
            "weight": 60,
            "stats": {
                "hp": 35,
                "attack": 55,
                "defense": 40,
                "special-attack": 50,
                "special-defense": 50,
                "speed": 90
            },
            "abilities": ["静电"]
        }
        
        mock_species = {
            "name": "皮卡丘",
            "flavor_text": "它脸颊上的电气袋里储存着发电的电力。当它生气时，电力会激增。",
            "habitat": "草原",
            "growth_rate": "中等快速",
            "evolution_chain": {
                "baby_trigger_item": None,
                "chain": {
                    "evolution_details": [],
                    "evolves_to": [{
                        "evolution_details": [{
                            "min_level": 25,
                            "trigger": {
                                "name": "level-up",
                                "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                            }
                        }],
                        "evolves_to": [],
                        "species": {
                            "name": "雷丘",
                            "url": "https://pokeapi.co/api/v2/pokemon-species/26/"
                        }
                    }],
                    "species": {
                        "name": "皮卡丘",
                        "url": "https://pokeapi.co/api/v2/pokemon-species/25/"
                    }
                }
            }
        }
        
        # 测试回答生成的token消耗
        print("\n2. 测试回答生成:")
        answer_result = await doubao_client.build_answer_with_doubao(
            question=user_question,
            pokemon_data={
                "name": "pikachu",
                "height": 4,
                "weight": 60,
                "types": [{"type": {"name": "electric"}}],
                "stats": [{"stat": {"name": "hp"}, "base_stat": 35}, {"stat": {"name": "attack"}, "base_stat": 55}, {"stat": {"name": "defense"}, "base_stat": 40}, {"stat": {"name": "special-attack"}, "base_stat": 50}, {"stat": {"name": "special-defense"}, "base_stat": 50}, {"stat": {"name": "speed"}, "base_stat": 90}],
                "abilities": [{"ability": {"name": "static"}, "is_hidden": False}],
                "moves": [{"move": {"name": "thunder-shock"}}]
            },
            species_data={
                "name": "pikachu",
                "capture_rate": 190,
                "base_happiness": 50,
                "growth_rate": {"name": "medium-fast"},
                "egg_groups": [{"name": "field"}],
                "color": {"name": "yellow"},
                "flavor_text_entries": [{"flavor_text": "它脸颊上的电气袋里储存着发电的电力。当它生气时，电力会激增。", "language": {"name": "zh-Hans"}}]
            }
        )
        print(f"回答生成结果: {answer_result}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试过程中发生错误: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_token_consumption())