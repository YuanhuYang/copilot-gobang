<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
项目: 五子棋 (Gobang) 纯标准库控制台程序。
需求要点:
- 不使用第三方依赖。
- 关注代码可读性、简洁性与稳定性。
- 模块划分: board / game / ai / exceptions / main。
- AI 仅需轻量启发式, 可考虑后续扩展 Alpha-Beta / MCTS，但默认保持快速。
- 保持跨平台 (Windows / Linux / macOS)。
- 未来测试放在 tests/，建议使用 pytest (尚未添加依赖)。
生成代码时请遵循已有风格: 类型注解、PEP8、简体中文注释。
