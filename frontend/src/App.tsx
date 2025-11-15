/**
 * 应用主组件：提供输入框与按钮，调用后端问答接口并展示结果。
 * 根据截图重新设计的宝可梦主题界面
 */
import React, { useState, useEffect } from "react";
import axios from "axios";

/**
 * Pokédex AI 主页
 * 使用截图中的新设计风格
 */
export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [pokemonName, setPokemonName] = useState<string | null>(null);
  const [pokemonId, setPokemonId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isMobile, setIsMobile] = useState(false);
  const [hasSubmitted, setHasSubmitted] = useState(false);
  
  // 检测屏幕尺寸变化
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 600);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  // 输入验证函数
  const validateQuestion = (text: string): boolean => {
    const trimmed = text.trim();
    return trimmed.length > 0 && trimmed.length <= 500;
  };

  /**
   * 调用后端问答接口
   * - 清理前次错误/答案
   * - 异步提交到 /api/v1/ask
   * - 根据返回更新 answer 或错误信息
   */
  const ask = async () => {
    // 验证输入
    if (!validateQuestion(question)) {
      setError("请输入有效问题（1-500个字符）");
      return;
    }
    
    setLoading(true);
    setError("");
    setAnswer("");
    setPokemonName(null);
    setPokemonId(null);
    setHasSubmitted(true);
    
    try {
      const res = await axios.post("/api/v1/ask", { question });
      setAnswer(res.data.answer ?? "");
      // 从API响应中获取宝可梦信息
      setPokemonName(res.data.pokemon_name || null);
      setPokemonId(res.data.pokemon_id || null);
    } catch (e: any) {
      // 更友好的错误处理
      if (e.response?.status === 400) {
        setError("输入问题无法理解，请尝试重新表述");
      } else if (e.response?.status === 404) {
        setError("未找到相关宝可梦信息，请检查是否正确拼写了宝可梦名称");
      } else if (e.response?.status === 500) {
        setError("服务器暂时无法处理请求，请稍后重试");
      } else {
        setError("网络连接问题，请检查您的网络并重试");
      }
      console.error("请求错误:", e);
    } finally {
      setLoading(false);
    }
  };

  // 解析回答内容，分离基本信息和分点内容
  const parseAnswer = () => {
    if (!answer) return { main: '', points: [] };
    
    try {
      // 第一步：清理所有Markdown标题标记
      let processedAnswer = answer.replace(/###\s*(整体概括|分点说明)\s*/g, '').trim();
      
      // 第二步：处理特定的皮卡丘种族值格式
      if (processedAnswer.includes('1. 皮卡丘为电属性宝可梦，其种族值及核心信息如下:')) {
        // 拆分所有行并过滤掉空行
        const allLines = processedAnswer.split('\n').map(line => line.trim()).filter(line => line);
        
        // 提取主要内容
        let mainContent = allLines[0].replace(/^\d+\.\s*/, '').trim();
        
        // 提取分点内容
        let points: string[] = [];
        
        // 遍历所有行，寻找真正的分点
        for (const line of allLines) {
          // 查找类似 "3. 1.属性：电属性" 这样的格式
          const nestedPointMatch = line.match(/^\d+\.\s*(\d+)\.(.+)$/);
          if (nestedPointMatch) {
            // 提取嵌套的分点内容
            points.push(nestedPointMatch[2].trim());
          }
          // 查找普通的分点格式，但排除空的分点
          else if (/^\d+\.\s+[^\s]/.test(line)) {
            // 提取分点内容，忽略行首的数字+点号
            const pointContent = line.replace(/^\d+\.\s*/, '').trim();
            if (pointContent) {
              points.push(pointContent);
            }
          }
        }
        
        // 如果没有找到分点，尝试提取属性和种族值信息
        if (points.length === 0) {
          // 直接查找属性、种族值、特性等信息
          const attributeMatch = processedAnswer.match(/属性：([^\n]+)/);
          const statsMatch = processedAnswer.match(/种族值：([^\n]+)/);
          const abilityMatch = processedAnswer.match(/特性：([^\n]+)/);
          
          if (attributeMatch) points.push(attributeMatch[0].trim());
          if (statsMatch) points.push(statsMatch[0].trim());
          if (abilityMatch) points.push(abilityMatch[0].trim());
        }
        
        return { main: mainContent, points };
      }
      // 处理普通的分点格式
      else if (/\n\s*\d+\.\s*/.test(processedAnswer)) {
        const lines = processedAnswer.split('\n').map(line => line.trim()).filter(line => line);
        
        // 第一行作为主要内容
        const mainContent = lines[0].replace(/^\d+\.\s*/, '').trim();
        
        // 提取分点
        const points = lines.slice(1)
          .map(line => {
            // 处理嵌套的分点格式
            const nestedMatch = line.match(/^\d+\.\s*(\d+)\.(.+)$/);
            if (nestedMatch) {
              return nestedMatch[2].trim();
            }
            // 处理普通分点格式
            return line.replace(/^\d+\.\s*/, '').trim();
          })
          .filter(p => p.length > 0);
        
        return { main: mainContent, points };
      }
      // 处理"整体："和"分点："格式
      else if (processedAnswer.includes('整体：') || processedAnswer.includes('分点：')) {
        // 提取主要内容
        const mainContent = processedAnswer.replace(/整体：/, '').split('分点：')[0].trim();
        
        // 提取分点内容
        const pointsMatch = processedAnswer.match(/分点：[\s\S]+/);
        let points: string[] = [];
        
        if (pointsMatch) {
          const pointsText = pointsMatch[0].replace('分点：', '').trim();
          points = pointsText.split(/\n/) 
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .map(line => line.replace(/^\d+\.\s*/, ''));
        }
        
        return { main: mainContent, points };
      }
      
      // 默认情况：返回清理后的内容
      return { 
        main: processedAnswer.trim(), 
        points: [] 
      };
    } catch (e) {
      console.error('解析回答失败:', e);
      // 错误处理：返回最基本的清理内容
      return { 
        main: answer.replace(/###\s*(整体概括|分点说明)\s*/g, '').trim(), 
        points: [] 
      };
    }
  };

  const { main, points } = parseAnswer();

  return (
    <div className="pokedex-app">
      {/* 橙色渐变标题栏 */}
      <div className="title-bar">
        <h1 className="app-title">Pokédex AI 智能图鉴系统</h1>
        <p className="app-subtitle">请提出关于宝可梦的任何问题！</p>
      </div>
      
      {/* 输入区域 */}
      <div className="input-section">
        <input
          className="question-input"
          placeholder={isMobile ? "输入宝可梦问题..." : "输入你的宝可梦问题，如：皮卡丘的属性和种族值？"}
          value={question}
          onChange={(e) => {
            setQuestion(e.target.value);
            // 输入时清除错误
            if (error) setError("");
          }}
          onKeyPress={(e) => e.key === 'Enter' && validateQuestion(question) && !loading && ask()}
          maxLength={500}
        />
        <div className="input-footer">
          <span className="char-count">{question.length}/500</span>
          <button 
            className={`submit-button ${
              !validateQuestion(question) && question ? 'invalid-input' : ''
            }`}
            onClick={ask} 
            disabled={!validateQuestion(question) || loading}
            title={!validateQuestion(question) && question ? "请输入有效问题" : "点击获取宝可梦信息"}
          >
            {loading ? "处理中..." : (isMobile ? "查询" : "获取信息")}
          </button>
        </div>
      </div>
      
      {/* 错误消息 - 增强版 */}
      {error && (
        <div className="error-box">
          <span className="error-icon">⚠️</span>
          <div className="error-content">
            <span className="error-text">{error}</span>
            <button 
              className="error-close"
              onClick={() => setError("")}
              aria-label="关闭错误信息"
            >
              ✕
            </button>
          </div>
        </div>
      )}
      
      {/* 空状态展示 */}
      {hasSubmitted && !answer && !error && !loading && (
        <div className="empty-state">
          <div className="empty-icon">🔮</div>
          <h3 className="empty-title">暂无相关信息</h3>
          <p className="empty-text">尝试提出不同的宝可梦问题，例如：</p>
          <div className="suggestions-list">
            <button 
              className="suggestion-item"
              onClick={() => {
                setQuestion("皮卡丘的特性是什么？");
                setHasSubmitted(false);
              }}
            >
              皮卡丘的特性是什么？
            </button>
            <button 
              className="suggestion-item"
              onClick={() => {
                setQuestion("喷火龙有几种进化形态？");
                setHasSubmitted(false);
              }}
            >
              喷火龙有几种进化形态？
            </button>
            <button 
              className="suggestion-item"
              onClick={() => {
                setQuestion("超梦的种族值是多少？");
                setHasSubmitted(false);
              }}
            >
              超梦的种族值是多少？
            </button>
          </div>
        </div>
      )}
      
      {/* 回答区域 - 增强版 */}
      {answer && !error && (
        <div className={`answer-section ${points.length > 0 ? 'has-points' : 'no-points'} ${isMobile ? 'mobile' : ''}`}>
          <h2 className="answer-title">
            {isMobile ? "回答" : "智能回答"}
            <span className="answer-status">✅</span>
          </h2>
          
          {/* 宝可梦识别信息 - 增强版 */}
          {(pokemonName || pokemonId) && (
            <div className="pokemon-info">
              <span className="pokemon-icon">{pokemonName ? '⚡' : '🔍'}</span>
              <div className="pokemon-details">
                {pokemonName && (
                  <span className="info-item">
                    <strong>{pokemonName}</strong>
                    {pokemonId !== null && <span className="pokemon-id">#{pokemonId}</span>}
                  </span>
                )}
              </div>
            </div>
          )}
          
          {/* 智能内容展示：根据内容复杂度自适应调整 */}
          <div className="content-container">
            {/* 主要内容 */}
            {main && (
              <div className={`main-content ${main.length > 100 ? 'long-content' : 'short-content'}`}>
                <p>{main}</p>
              </div>
            )}
            
            {/* 分点内容 - 增强版 */}
            {points.length > 0 && (
              <div className="points-container">
                <h3 className="points-title">
                  {isMobile ? "详情" : "详细信息"}
                  <span className="points-count">({points.length})</span>
                </h3>
                <ul className="points-list">
                  {points.map((point, index) => (
                    <li key={index} className={`point-item ${index % 2 === 0 ? 'even' : 'odd'}`}>
                      <span className="point-number">{index + 1}.</span>
                      <span className="point-text">{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
      
      {/* 加载状态 - 增强版 */}
      {loading && (
        <div className="loading-section">
          <div className="loading-animation">
            <div className="loading-spinner"></div>
            <div className="loading-pokeball"></div>
          </div>
          <p className="loading-text">正在为您分析宝可梦数据...</p>
          <p className="loading-subtext">请稍候，智能图鉴正在努力工作中</p>
        </div>
      )}
      
      {/* 版本信息 */}
      <div className="version-info">
        基于PokeAPI与AI技术构建 | v1.1.0
      </div>
      
      <style>{`
        /* 全局样式 */
        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }
        
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
          background-color: #f0f2f5;
          line-height: 1.5;
        }
        
        /* 主容器 */
        .pokedex-app {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        
        /* 橙色渐变标题栏 */
        .title-bar {
          background: linear-gradient(90deg, #ff6b35 0%, #f7c95e 100%);
          border-radius: 12px;
          padding: 25px 30px;
          text-align: center;
          color: white;
          box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
        }
        
        .app-title {
          font-size: 28px;
          font-weight: bold;
          margin-bottom: 8px;
          text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .app-subtitle {
          font-size: 16px;
          opacity: 0.9;
          font-weight: 500;
        }
        
        /* 输入区域 */
        .input-section {
          background: white;
          border-radius: 12px;
          padding: 25px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          display: flex;
          flex-direction: column;
          gap: 15px;
        }
        
        /* 输入底部信息 */
        .input-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 10px;
        }
        
        /* 字符计数 */
        .char-count {
          font-size: 12px;
          color: #999;
          min-width: 60px;
          text-align: right;
        }
        
        /* 无效输入按钮样式 */
        .submit-button.invalid-input {
          opacity: 0.8;
        }
        
        .submit-button.invalid-input:hover:not(:disabled) {
          background: linear-gradient(90deg, #ff4d4f 0%, #ff7875 100%);
        }
        
        .question-input {
          padding: 15px 20px;
          border: 1px solid #d9d9d9;
          border-radius: 8px;
          font-size: 16px;
          outline: none;
          transition: border-color 0.3s;
        }
        
        .question-input:focus {
          border-color: #1890ff;
          box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
        }
        
        /* 蓝色按钮 */
        .submit-button {
          background: linear-gradient(90deg, #1890ff 0%, #40a9ff 100%);
          color: white;
          border: none;
          padding: 15px 20px;
          border-radius: 8px;
          font-size: 16px;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.3s;
        }
        
        .submit-button:hover:not(:disabled) {
          background: linear-gradient(90deg, #40a9ff 0%, #69c0ff 100%);
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
        }
        
        .submit-button:disabled {
          background: #f5f5f5;
          color: #bfbfbf;
          cursor: not-allowed;
        }
        
        /* 错误消息 - 增强版 */
        .error-box {
          background: #fff2f0;
          border: 1px solid #ffccc7;
          border-radius: 8px;
          padding: 15px 20px;
          color: #ff4d4f;
          display: flex;
          align-items: center;
          gap: 8px;
          animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .error-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex: 1;
        }
        
        .error-close {
          background: none;
          border: none;
          color: #ff4d4f;
          cursor: pointer;
          font-size: 16px;
          padding: 2px 6px;
          border-radius: 4px;
          transition: all 0.2s;
        }
        
        .error-close:hover {
          background: #ffccc7;
          transform: scale(1.1);
        }
        
        /* 回答区域 - 增强版 */
        .answer-section {
          background: white;
          border-radius: 12px;
          padding: 25px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          transition: all 0.3s ease;
          animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .answer-section.has-points {
          background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
          border-left: 4px solid #40a9ff;
        }
        
        .answer-section.mobile {
          padding: 20px;
        }
        
        .answer-title {
          font-size: 20px;
          font-weight: bold;
          color: #262626;
          margin-bottom: 20px;
          padding-bottom: 10px;
          border-bottom: 2px solid #f0f0f0;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        
        .answer-status {
          font-size: 16px;
          opacity: 0.7;
        }
        
        /* 宝可梦信息 - 增强版 */
        .pokemon-info {
          background: linear-gradient(135deg, #f6ffed 0%, #f0f9ff 100%);
          border-radius: 8px;
          padding: 12px 16px;
          margin-bottom: 20px;
          display: flex;
          align-items: center;
          gap: 12px;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
          border: 1px solid #e6f7ff;
        }
        
        .pokemon-icon {
          font-size: 20px;
          opacity: 0.8;
        }
        
        .pokemon-details {
          flex: 1;
        }
        
        .info-item {
          font-size: 14px;
          color: #666;
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 500;
        }
        
        .info-item strong {
          color: #1890ff;
          font-weight: 600;
          font-size: 16px;
        }
        
        .pokemon-id {
          background: #1890ff;
          color: white;
          padding: 2px 6px;
          border-radius: 10px;
          font-size: 12px;
          font-weight: 600;
        }
        
        /* 内容容器 */
        .content-container {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        
        /* 主要内容 - 根据长度动态调整 */
        .main-content {
          line-height: 1.7;
          padding: 15px;
          border-radius: 8px;
          transition: all 0.3s ease;
        }
        
        .main-content p {
          margin: 0;
          color: #262626;
          font-size: 16px;
        }
        
        .main-content.short-content {
          background: #e6f7ff;
          border-left: 3px solid #1890ff;
        }
        
        .main-content.long-content {
          background: #f6ffed;
          border-left: 3px solid #52c41a;
          font-size: 15px;
          line-height: 1.8;
        }
        
        /* 分点内容容器 - 增强版 */
        .points-container {
          margin-top: 10px;
        }
        
        .points-title {
          font-size: 16px;
          font-weight: 600;
          color: #262626;
          margin-bottom: 15px;
          display: flex;
          align-items: center;
          gap: 6px;
        }
        
        .points-title::before {
          content: "📋";
          font-size: 14px;
        }
        
        .points-count {
          font-size: 12px;
          color: #999;
          font-weight: normal;
        }
        
        .points-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        
        .point-item {
          display: flex;
          align-items: flex-start;
          gap: 8px;
          padding: 12px;
          border-radius: 6px;
          transition: all 0.2s ease;
        }
        
        .point-item:hover {
          transform: translateX(4px);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .point-item.even {
          background: #f0f9ff;
          border-left: 2px solid #91d5ff;
        }
        
        .point-item.odd {
          background: #f6ffed;
          border-left: 2px solid #b7eb8f;
        }
        
        .point-number {
          font-weight: bold;
          color: #1890ff;
          font-size: 14px;
          min-width: 20px;
          text-align: right;
        }
        
        .point-text {
          flex: 1;
          color: #595959;
          font-size: 14px;
          line-height: 1.6;
        }
        
        /* 加载状态 - 增强版 */
        .loading-section {
          background: white;
          border-radius: 12px;
          padding: 40px 25px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 15px;
          min-height: 200px;
        }
        
        .loading-animation {
          position: relative;
          width: 60px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .loading-spinner {
          width: 40px;
          height: 40px;
          border: 3px solid #f0f0f0;
          border-top: 3px solid #1890ff;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          position: absolute;
        }
        
        .loading-pokeball {
          width: 20px;
          height: 20px;
          background: radial-gradient(circle, #fff 30%, transparent 30%), radial-gradient(circle, #ff4d4f 50%, #fff 50%);
          border-radius: 50%;
          animation: pulse 1.5s ease-in-out infinite;
        }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.2); opacity: 0.8; }
        }
        
        .loading-text {
          color: #666;
          font-size: 16px;
          font-weight: 500;
          margin: 0;
        }
        
        .loading-subtext {
          color: #999;
          font-size: 12px;
          margin: 0;
          text-align: center;
        }
        
        /* 空状态样式 */
        .empty-state {
          background: white;
          border-radius: 12px;
          padding: 40px 25px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          text-align: center;
          min-height: 200px;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 15px;
        }
        
        .empty-icon {
          font-size: 48px;
          opacity: 0.7;
        }
        
        .empty-title {
          font-size: 18px;
          font-weight: 600;
          color: #262626;
          margin: 0;
        }
        
        .empty-text {
          font-size: 14px;
          color: #666;
          margin: 0;
        }
        
        .suggestions-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
          width: 100%;
          max-width: 300px;
          margin-top: 10px;
        }
        
        .suggestion-item {
          background: #f5f5f5;
          border: 1px solid #d9d9d9;
          border-radius: 6px;
          padding: 10px 15px;
          font-size: 14px;
          color: #595959;
          cursor: pointer;
          transition: all 0.2s ease;
          text-align: left;
        }
        
        .suggestion-item:hover {
          background: #e6f7ff;
          border-color: #91d5ff;
          transform: translateX(4px);
        }
        
        /* 版本信息 */
        .version-info {
          text-align: center;
          font-size: 12px;
          color: #bfbfbf;
          margin-top: auto;
          padding-top: 20px;
        }
        
        /* 响应式设计 */
        @media (max-width: 600px) {
          .pokedex-app {
            padding: 15px;
          }
          
          .title-bar {
            padding: 20px;
          }
          
          .app-title {
            font-size: 24px;
          }
          
          .input-section,
          .answer-section {
            padding: 20px;
          }
        }
      `}</style>
    </div>
  );
}