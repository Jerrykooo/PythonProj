import csv

csvFile = open("instance.csv", "a+", newline='')

# 文件头以列表的形式传入函数，列表的每个元素表示每一列的标识
fileheader = ["name", "score"]
dict_writer = csv.DictWriter(csvFile, fileheader)

# 但是如果此时直接写入内容，会导致没有数据名，所以，应先写数据名（也就是我们上面定义的文件头）。
# 写数据名，可以自己写如下代码完成：

dict_writer.writerow(dict(zip(fileheader, fileheader)))

# 之后，按照（属性：数据）的形式，将字典写入CSV文档即可
dict_writer.writerow({"name": "Li", "score": "80"})

csvFile.close()