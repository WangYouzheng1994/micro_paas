# 工具目标

> 通用多实例监控与消息通知系统。支持 MySQL/Redis/等常见IO操作服务，消息通道支持钉钉、企业微信。  

- 使用方式：通过 **Poetry** 打包部署，使用 **cron** 定时运行。

> 项目使用Poetry (version 2.1.4)开发的
> python版本3.12

### 打包与安装使用方式

```shell
poetry build # 打包
# 打包命令执行后会在工程目录下生成dist目录，其中有.tar和.whl文件

whl文件上传到服务器
pip install dist/project-0.0.1-py3-none-any.whl
```

### 服务器部署方式

---

## 本地调试
```shell
# 再项目根目录执行，可以触发cli.py中的脚本。
poetry run monitor check-all --config ./config/config.yaml

# 这个表示是通过poetry 来运行python命令，为什么要这样？因为环境变量给抽取出来了，可以认为就是idea的target的能力。
# 废弃，直接run 方便点 

poetry run python -m project.main
```

---
### 尼玛，踩过的坑。。。企业级项目还是java生态完善。。。o(╥﹏╥)o
#### Poetry，安装结束后，需要知道的命令。
```
toml文件就是maven的pom

poetry install  # 等价于 yarn install
poetry add xxxx # 等价于 yarn add xxxx
poetry lock # 根据toml文件生成lock文件

```

### vs code 资源更少。。适应适应熊迪们

| 功能     | PyCharm            | VS Code (默认)                  |
| ------ | ------------------ | ----------------------------- |
| 格式化代码  | `Ctrl+Alt+L`       | `Shift+Alt+F`（可修改）            |
| 查找文件   | `Ctrl+Shift+N`     | `Ctrl+P`                      |
| 查找类    | `Ctrl+N`           | `Ctrl+T`                      |
| 查找方法   | `Ctrl+Shift+Alt+N` | `Ctrl+Shift+O`                |
| 显示最近文件 | `Ctrl+E`           | `Ctrl+R`                      |
| 注释代码   | `Ctrl+/`           | `Ctrl+/`（Python 同样适用）         |
| 多行编辑   | `Alt+J`            | `Ctrl+D` 或 `Ctrl+Alt+Down/Up` |
| 跳转定义   | `Ctrl+B`           | `F12`                         |

---