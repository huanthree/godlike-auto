# Auto Renew streamlit

自动续期streamlit的脚本，使用 GitHub Actions 每12小时自动运行一次。

## 功能特点

- 自动点击streamlit运行
- 自动点击续期按钮
- 验证续期是否成功
- 每12小时自动运行
- telegram消息推送
- 支持手动触发运行

## 使用方法


### 2. 设置 GitHub Actions

1. Fork 这个仓库
2. 在仓库中设置 Secret：
3. telegram消息推送功能可选，如需要请在secrets中添加```TELEGRAM_BOT_TOKEN```和```TELEGRAM_CHAT_ID```环境变量

### 3. 验证运行

- Actions 将每96小时(4天)自动运行一次
- 您可以在 Actions 页面查看运行状态和日志
- 需要立即运行时，可以在 Actions 页面手动触发

## 注意事项

- 请确保 cookie及邮箱密码正确
- 建议定期检查 Actions 运行日志，确保脚本正常运行
- 如果需要修改运行频率，可以调整 `.github/workflows/auto_renew.yml` 中的 cron 表达式
