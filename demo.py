def swap(data, root, last):
    data[root], data[last] = data[last], data[root]


# 调整父节点 与孩子大小， 制作大顶堆
def addjust_head(data, par_node, high):
    new_par_node = par_node
    j = 2 * par_node + 1  # 取根节点的左孩子， 如果只有一个孩子 high就是左孩子，如果有两个孩子 high 就是右孩子

    while j <= high:  # 如果 j = high 说明没有右孩子，high就是左孩子
        if j < high and data[j] < data[j + 1]:  # 如果这儿不判断 j < high 可能超出索引
            # 一个根节点下，如果有两个孩子，将 j  指向值大的那个孩子
            j += 1
        if data[j] > data[new_par_node]:  # 如果子节点值大于父节点，就互相交换
            data[new_par_node], data[j] = data[j], data[new_par_node]
            new_par_node = j  # 将当前节点，作为父节点，查找他的子树
            j = j * 2 + 1

        else:
            # 因为调整是从上到下，所以下面的所有子树肯定是排序好了的，
            # 如果调整的父节点依然比下面最大的子节点大，就直接打断循环，堆已经调整好了的
            break


# 索引计算: 0 -->1 --->....
#    父节点 i   左子节点：偶数:2i +1  右子节点：基数:2i +2  注意：当用长度表示最后一个叶子节点时 记得 -1

# 从第一个非叶子节点(即最后一个父节点)开始，即 list_.length//2 -1（len(list_)//2 - 1）
# 开始循环到 root 索引为：0 的第一个根节点， 将所有的根-叶子 调整好，成为一个 大顶堆
def heap_sort(lst):
    """
    根据列表长度，找到最后一个非叶子节点，开始循化到 root 根节点，制作 大顶堆
    :param lst: 将列表传入
    :return:
    """
    length = len(lst)
    last = length - 1  # 最后一个元素的 索引
    last_par_node = length // 2 - 1

    while last_par_node >= 0:
        addjust_head(lst, last_par_node, length - 1)
        last_par_node -= 1  # 每调整好一个节点，从后往前移动一个节点
    print(lst)
    # return lst
    while last > 0:
        #
        # swap(lst, 0, last)
        lst[0], lst[last] = lst[last], lst[0]
        # 调整堆少让 adjust 处理最后已经排好序的数，就不处理了
        addjust_head(lst, 0, last - 1)
        last -= 1

    return lst  # 将列表返回


list_ = [4, 7, 0, 9, 1, 5, 3, 3, 2, 6, 100, 33]

heap_sort(list_)
print(list_)
import os
print(os.listdir('D:/WR-GameServer/gameaidb/DB'))
