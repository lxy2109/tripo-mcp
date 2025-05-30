# Tripo3D MCP 工具集成（本地/CLI 版）

本项目基于 Tripo3D 官方 API 封装，支持文本/图片/多视图转3D、贴图、动画、风格化、格式转换、余额查询等全流程。适用于 AI 3D 生成、AIGC 平台、Cursor 本地开发等场景。

---

## 功能特性
- 文本/图片/多视图转3D模型
- 模型贴图、动画绑定与重定向
- 风格化、格式转换、余额查询
- 全参数建模，自动类型校验
- 支持异步、易于扩展
- 适配本地 CLI/Cursor 环境

## 目录结构
```
tripo-mcp/
├── src/
│   ├── main.py           # 工具调用入口（服务主程序）
│   ├── tripo_api.py      # Tripo3D API 封装（异步）
│   ├── models.py         # Pydantic参数建模
│   ├── config.py         # API基础配置
│   └── __init__.py
├── requirements.txt      # 依赖包列表
├── pyproject.toml        # Python 项目元数据与依赖
├── mcp.json.example      # MCP本地服务配置示例
├── .gitignore
└── README.md
```

## 环境要求

- 操作系统：Windows、Linux 或 macOS
- Python 版本：推荐 Python 3.8 及以上
- 依赖包：详见 requirements.txt 或 pyproject.toml
```

## 克隆包体
```bash
git clone @https://github.com/lxy2109/tripo-mcp.git
```

## 安装依赖
```bash
pip install -r src/requirements.txt
```

## 环境变量配置
请在项目根目录创建 `.env` 文件，内容如下：
```
TRIPO_API_KEY=你的Tripo3D_API_Key
```
> ⚠️ 建议不要将API Key硬编码在config.py，生产环境请用.env或环境变量管理。

## mcp.json 配置说明

如需在 Cursor 或本地环境下自动运行服务，请在项目根目录新建 `mcp.json`，内容如下（可参考 mcp.json.example）：

```json
{
  "mcpServers": {
    "tripo-mcp": {
      "command": "python",
      "args": [
        "你的绝对或相对路径/tripo-mcp/src/main.py"
      ],
      "env": {
        "TRIPO_API_KEY": "你的Tripo3D_API_Key"
      },
      "url": "http://localhost:5001/mcp"
    }
  }
}
```
- `command`：启动主程序的命令（通常为 `python`）。
- `args`：主程序路径（建议用绝对路径或相对路径）。
- `env`：环境变量，需包含 `TRIPO_API_KEY`。
- `url`：本地服务监听地址（如有 HTTP 服务，可指定端口和路径）。

## 启动方法
直接运行 main.py 即可：
```bash
python src/main.py
```
或通过 Cursor/CLI 工具自动调用。

## 典型用法（自然语言调用示例）

你可以在 Cursor 的命令面板或 CLI 工具中直接用自然语言描述你的需求，例如：

- "用文本生成一个卡通小猫的3D模型"
- "将这张图片转成3D模型，风格为写实"
- "查询当前账户的 Tripo3D API 余额"
- "把模型转换为 FBX 格式并下载"
- "给这个模型加上动画骨骼并导出"
- "查询任务ID为 xxx 的处理进度"

只需用中文或英文描述你的目标，工具会自动解析并调用对应的 Tripo3D 能力。

## 常见问题
- **API Key未生效**：请检查.env文件或mcp.json中的环境变量是否正确加载。
- **依赖安装失败**：建议使用 Python 3.8+，并确保 pip 源可用。
- **网络异常**：请确保本地网络可访问 Tripo3D 官方 API。

## 参考
- [Tripo3D 官方文档](https://platform.tripo3d.ai/docs)

---

如有问题欢迎提 Issue 或 PR！ 