import pickle


def pre_order_tree(tree, path):
    if tree.nodeStatus == 0:
        labels = tree.label.ravel()
        if len(labels) > 0:
            print(path, max(list(labels), key=list(labels).count))
    else:
        pre_order_tree(tree.LeftChild, path+'0')
        pre_order_tree(tree.RightChild, path+'1')


TREE_ID = 1

tree = model.trees[TREE_ID]
pre_order_tree(tree, '')
