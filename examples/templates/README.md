# Templates

这个目录提供的是“迁移一个新模型”时最先复制的模板，而不是最终标准答案。

推荐顺序：

1. 先复制 `recipe.yaml`
2. 再补 `README.md`
3. 再补 `run.sh` 或 `run.py`
4. 再补依赖文件
5. 再补 `run.json`
6. 最后补 `profiling.json`

完成后运行：

```bash
PYTHONPATH=src python3 -m auto_analysis_tool validate
PYTHONPATH=src python3 -m auto_analysis_tool report
```
