# relay-story 多人接力故事

指由读者/作者参与后续剧情撰写与推进。采用多分支方式以满足不同读者/作者对于不同情节的偏好。

## 背景

本项目由BobAnkh发起，旨在搭建多分支接力小说的框架。从任何一个已有节点，所有读者/作者都可以在新文件中以符合要求的方式续写你所想的剧情

## 使用说明

### 安装说明

使用`pip install relaystory`进行安装，使用方式如下：

```console
usage: relaystory [-h] [-i INPUT] [-o OUTPUT] [-f FORMAT [FORMAT ...]]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        directory contains the src markdown files. Default to story.
  -o OUTPUT, --output OUTPUT
                        directory to output all the generated stories. Default to output.
  -f FORMAT [FORMAT ...], --format FORMAT [FORMAT ...]
                        select the output format. Options: all, markdown, html, pdf. Default to markdown.
```

例如运行`relaystory -i story -o output -f markdown`命令，可将`story`文件夹下的按一定格式组织的文件组织成故事，并以**markdown**的格式输出在文件夹`output/markdown`下。

具体可参见[本仓库](https://github.com/BobAnkh/relay-story)下`story`和`output`文件夹中的示例，也欢迎为此示例贡献。

### 文件规范

所有文件将全部存放于同一个文件夹中，并按照一下规范进行组织。

#### 文件命名

对于每一段故事，采用`<级别>.<序号>`的命名方式，其后无需跟随任何内容。`<级别>`指的是故事的层级，例如初始节点即为级别1，接着初始节点故事所写的故事即为级别2，以此类推。`<序号>`仅作为同一级别中区分各文件用。如第二级的故事(指其上游已有两次情节)，命名形如`2.1`。

#### 文件内容

故事采用markdown进行撰写，需在文中任意一些行以下述注释形式指出一下元数据:

- 上游编号(即被续接的故事的文件名): `<!--upstream: x.y-->`. 如`<!--upstream: 2.1-->`
- 作者: `<!--author: YourName-->`. 如`<!--author: BobAnkh-->`
- 书名(最终合并完成的书籍以最后一个节点的书名为准): `<!--book name: YourBookName-->`. 如`<!--book name: DarkSouls-->`
- 章节名(会覆盖掉内容中首个一级标题的内容, 如'# title', 若无则添加为一级标题. 即章节标题以此为准, 建议内容中一级标题与此相同): `<!--chapter name: YourChapterName-->`. `<!--chapter name: ch01-->`

## 维护者

[@BobAnkh](https://github.com/BobAnkh)

## 如何贡献

我们非常欢迎任何人为本项目贡献自己的力量，为这个仓库添加新的内容，只要它对于这个仓库是具有意义的，并且是符合规范的。

欢迎随时提出issue或者提交pull request，但是它们需要按照各自的template进行填写。

可以优先考虑具有`help wanted`标签的issue。

同时请注意，参与本项目需要遵守[Code of Conduct](/CODE_OF_CONDUCT.md)。

对于本仓库的示例故事可以按照使用说明任意进行贡献。

## 使用许可

[Apache-2.0](/LICENSE) © BobAnkh
