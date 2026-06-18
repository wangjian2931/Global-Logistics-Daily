# global-logistics-daily

全球物流（Global Logistics）每日资讯：国际货代 + EPC 工程物流，DeepSeek 摘要，Buttondown 邮件，GitHub Pages 落地页。

## 微信分享链接

https://wangjian2931.github.io/global-logistics-daily/

## 首次配置 GitHub Pages（只需做一次）

1. 打开 https://github.com/wangjian2931/global-logistics-daily/settings/pages
2. **Build and deployment → Source** 选 **GitHub Actions**
3. 保存

## 推送代码并发布

```powershell
cd "C:\Wang Jian's files待转新机\cursor folder\global-logistics-daily"
git add .
git commit -m "update base url after repo rename"
git pull origin main --no-rebase
git push origin main
```

然后：**Actions → Run workflow**

## GitHub Secrets

- `DEEPSEEK_API_KEY`
- `BUTTONDOWN_API_KEY`

## 修改信息源

编辑 `config/sources.yaml`

## 修改落地页文案

编辑 `config/site.yaml`
