打包：

```bash
docker build -t easyjob:latest .
```

运行：

```bash
#!/bin/bash

# 环境变量
SESSION_ID=
ACCESS_TOKEN=

# 指定仓库
REPO_HOST=ghcr.1ms.run

# 执行脚本
docker pull "$REPO_HOST/jiehui555/easyjob:latest"
docker run --rm \
    -e SESSION_ID="$SESSION_ID" \
    -e ACCESS_TOKEN="$ACCESS_TOKEN" \
    "$REPO_HOST/jiehui555/easyjob:latest"
```
