# coding: utf-8


max_w = 0


def get_progress(current_step):
    return '=='*(current_step+1)*2 + 'step: ' + str(current_step)



def knapsack(current_step, current_weight, items, total_step, total_weight):
    print(get_progress(current_step))
    # print('current step: {}, current_weight: {}'.format(current_step, current_weight))
    # print('current items: {}'.format())
    global max_w

    if current_weight == total_weight or current_step == total_step:
        if current_weight > max_w:
            max_w = current_weight
        if current_weight == total_weight:
            print(get_progress(current_step), '重量为{}，返回'.format(total_weight))
            # print('**********************************************')
            return
        if current_step == total_step:
            print(get_progress(current_step), '达到步数，返回')
            # print('**********************************************')
            return

    print(get_progress(current_step), '不装物品，下一步')
    knapsack(current_step+1, current_weight, items, total_step, total_weight)

    if current_weight + items[current_step] <= total_weight:
        print(get_progress(current_step), '未超重，增加物品，下一步')
        print(get_progress(current_step), 'current weight:', current_weight, 'add weight:', items[current_step])
        knapsack(current_step+1, current_weight+items[current_step], items, total_step, total_weight)
    else:
        print(get_progress(current_step), '超重，不增加物品')

    # print('**********************************************')


if '__main__' == __name__:
    knapsack(0, 0, [2, 2, 4, 6, 4], 5, 11)
    print(max_w)