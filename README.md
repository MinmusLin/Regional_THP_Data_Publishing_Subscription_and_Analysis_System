# Regional THP Data Publishing Subscription and Analysis System

## 项目名称

Regional_THP_Data_Publishing_Subscription_and_Analysis_System

## 项目简介

Regional temperature / humidity / pressure data publishing, subscription, and analysis processing system.

某区域温度 / 湿度 / 气压数据发布订阅及分析处理系统。

> ***Relevant course***
> * Fundamentals of IoT Applications 2024 (2024年同济大学物联网应用基础)

## 成员信息

| 姓名 | 学号 |
| :---: | :---: |
| 林继申 | 2250758 |
| 刘淑仪 | 2251730 |
| 文达 | 2252934 |
| 蔡永怡 | 2254156 |
| 吴昊泽 | 2254269 |

```
git log --format='%aN' | sort -u | while read name; do echo -en "$name\t"; git log --author="$name" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s\n", add, subs, loc }' -; done
```

## 项目组成

* `/mqtt-server`
MQTT 服务端

* `/publisher-end`
发布端

* `/subscriber-end`
订阅端

## 免责声明

The code and materials contained in this repository are intended for personal learning and research purposes only and may not be used for any commercial purposes. Other users who download or refer to the content of this repository must strictly adhere to the **principles of academic integrity** and must not use these materials for any form of homework submission or other actions that may violate academic honesty. I am not responsible for any direct or indirect consequences arising from the improper use of the contents of this repository. Please ensure that your actions comply with the regulations of your school or institution, as well as applicable laws and regulations, before using this content. If you have any questions, please contact me via [email](mailto:minmuslin@outlook.com).

本仓库包含的代码和资料仅用于个人学习和研究目的，不得用于任何商业用途。请其他用户在下载或参考本仓库内容时，严格遵守**学术诚信原则**，不得将这些资料用于任何形式的作业提交或其他可能违反学术诚信的行为。本人对因不恰当使用仓库内容导致的任何直接或间接后果不承担责任。请在使用前务必确保您的行为符合所在学校或机构的规定，以及适用的法律法规。如有任何问题，请通过[电子邮件](mailto:minmuslin@outlook.com)与我联系。

## 文档更新日期

2024年12月20日