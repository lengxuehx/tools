## 1. 相关分支

  * 两个长期分支：master和dev， master用于发布，不允许直接提交代码，只接受来自dev分支和hotfix/xxx的merge； dev是任何新的特性开发的基础分支

  * 特性分支： 临时分支，任何新的功能开发应当基于dev创建新的特性分支feature/xxx，完成代码并测试后提交target为dev分支的merge request，经review后完成merge，merge后删除该feature/xxx分支

  * 修复分支： 临时分支，dev分支上发现bug后，相关人员基于dev分支创建修复分支fix/xxx，完成代码并测试后提交target为dev分支的merge request，经review后完成merge，merge后删除该fix/xxx分支(小的fix可以直接在dev分支上提交)

  * 热修复分支： 临时分支，已经发布的代码如果发现bug，相关人员基于master创建新的热修复分支hotfix/xxx，完成测试后提交target为master分支的merge request，经review后merge到master分支， 并cherry-pick到dev分支

## 2. 研发流程

   1. 某轮迭代开始，研发人员基于dev分支创建不同的feature/xxx分支，功能完成并自测试后提交merge request到dev分支，经review后完成merge

   2. 本轮迭代的所有功能完成后，测试人员按照需求对dev分支进行详细测试

   3. 测试完成后，dev分支merge到master分支并发布

   4. 如果发布代码发现bug，基于master创建hotfix/xx分支，测试完毕后提交merge request到master分支，经review后完成merge并发布

 ps： 该流程参考了[这篇文章](https://www.git-tower.com/learn/git/ebook/cn/command-line/advanced-topics/git-flow)