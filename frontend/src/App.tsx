/**
 * 应用主组件：提供输入框与按钮，调用后端问答接口并展示结果。
 */
import React, { useState } from "react";
import axios from "axios";

/**
 * Pokédex AI 主页
 */
export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /**
   * 调用后端问答接口
   * - 清理前次错误/答案
   * - 异步提交到 /api/v1/ask
   * - 根据返回更新 answer 或错误信息
   */
  const ask = async () => {
    setLoading(true);
    setError("");
    setAnswer("");
    try {
      const res = await axios.post("/api/v1/ask", { question });
      setAnswer(res.data.answer ?? "");
    } catch (e: any) {
      setError(e?.response?.data?.error?.message || e.message || "请求失败");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 720, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Pokédex AI</h1>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          style={{ flex: 1, padding: 8 }}
          placeholder="输入你的宝可梦问题，如：皮卡丘的属性和种族值？"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={ask} disabled={!question || loading}>
          {loading ? "处理中..." : "提问"}
        </button>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {answer && (
        <div style={{ marginTop: 16 }}>
          <h3>回答</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}