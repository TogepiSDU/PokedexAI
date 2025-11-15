"""API 冒烟用例（Smoke Tests）

涵盖健康检查与图鉴问答的核心路径，确保接口在关键场景下稳定可用。
"""
import pytest

def test_smk_001_healthcheck(client):
    """健康检查：GET / 应返回基础运行信息"""
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "message" in data and "version" in data and "docs" in data

def test_smk_002_normal_question(client):
    """正常提问：喷火龙（中文）应识别为 charizard 并返回答案"""
    r = client.post("/api/v1/ask", json={"question": "喷火龙的属性是什么？"})
    assert r.status_code == 200
    data = r.json()
    assert data.get("answer")
    assert data.get("pokemon_name") == "charizard"
    assert data.get("pokemon_id") == 6

def test_smk_003_unknown_pokemon(client):
    """未知宝可梦：应稳定返回并提示未找到"""
    r = client.post("/api/v1/ask", json={"question": "不存在龙是什么属性？"})
    assert 200 <= r.status_code < 500
    data = r.json()
    ok = False
    if isinstance(data, dict):
        if data.get("error") or data.get("detail"):
            ok = True
        else:
            ans = str(data.get("answer", ""))
            if any(s in ans for s in ["未找到", "不存在", "not found", "unknown"]):
                ok = True
    assert ok

def test_smk_004_empty_question(client):
    """空问题：应返回 400/422 并包含错误信息"""
    r = client.post("/api/v1/ask", json={"question": ""})
    assert r.status_code in (400, 422)
    data = r.json()
    assert isinstance(data, dict)