# 文件管理基础命令参考

## 常用命令

### 浏览目录
```bash
ls -la                    # 列出所有文件和详细信息
tree -L 2                 # 显示目录树（2层深度）
du -sh *                  # 显示所有项目的大小
pwd                       # 显示当前工作目录
```

### 文件操作
```bash
mv source dest            # 移动/重命名
cp source dest            # 复制
rm file                   # 删除文件
rm -rf directory          # 删除目录（递归+强制）
mkdir -p dir/subdir       # 创建目录（包括父目录）
touch file.txt            # 创建空文件
```

### 搜索文件
```bash
find . -name "*.txt"       # 按名称搜索
find . -type f -size +100M # 查找大于100MB的文件
find . -mtime -7           # 最近7天修改的文件
grep -r "text" .           # 在文件中搜索文本
```

### 文件信息
```bash
stat filename              # 详细文件信息
ls -lh filename            # 简要信息
file filename              # 文件类型
wc -l filename             # 行数统计
```

### 权限管理
```bash
chmod +x script.sh         # 添加执行权限
chmod 755 directory        # 设置权限
chown user:group file      # 修改所有者
```

### 批量操作
```bash
# 批量重命名
for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# 批量移动
mv *.pdf /docs/

# 批量删除
find . -name "*.tmp" -delete
```

## 安全注意事项

1. **删除前确认** - 使用 `ls` 检查要删除的文件
2. **递归删除** - `rm -rf` 非常危险，使用前确认
3. **通配符扩展** - 测试 `echo *.txt` 看看会匹配什么
4. **重要文件备份** - 操作前备份重要数据
5. **系统路径** - `/usr`, `/etc`, `/bin` 等需谨慎
