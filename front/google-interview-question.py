# 题目描述
# 长度为N的数组乱序存放这0到N-1，现在只能进行0与其他数的swap，请设计并实现排序

arr = [2,5,6,1,3,4,8,0,7]
arr_len = len(arr)
total_time = 0

def swap(a, b):
    if arr[a] != 0 and arr[b] != 0:
        print("error")
        return
    arr[a], arr[b] = arr[b], arr[a]
    print(arr)
    global total_time
    total_time = total_time + 1

def hannuota(a, b):
    swap(0, b)
    swap(a, b)
    swap(0, a)

def get_zero():
    for i in range(arr_len):
        if arr[i] == 0:
            swap(i, 0)
            break

def do_while():
    cnt = 1
    while cnt < arr_len:
        if arr[cnt] == cnt:
            cnt = cnt + 1
            continue
        hannuota(cnt, arr[cnt])
        
def main():
    # get 0
    get_zero()
    do_while()
    print('total time', total_time)



if __name__ == '__main__':
    main()