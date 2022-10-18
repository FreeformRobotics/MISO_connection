from scipy.special import comb
import pickle

def loop_rec(residue, x_previous, m):
    if m >= 1:
        for globals()['x' + str(m)] in range(1, min((residue-(m-1),x_previous))+1):
            loop_rec(residue-globals()['x' + str(m)], globals()['x' + str(m)], m - 1)
    else:
        if residue==0:
            list=[]
            for i in range(1, m_0 + 1):
                list.append(globals()['x' + str(i)])
            print(list)
            set_b = set(list)
            configuration_n=1
            for each_b in set_b:
                count = 0
                for each_a in list:
                    if each_b == each_a:
                        count += 1
                if count>1:
                    c = int(comb(count + space_volume[each_b] - 1, count))
                    print('the number {} is repeated by {} times, created {} configurations.'.format(each_b, count, c))
                    configuration_n=configuration_n*c
                else:
                    configuration_n=configuration_n*space_volume[each_b]
            print('total configuration number:{}'.format(configuration_n))
            global one_loop_result
            one_loop_result=one_loop_result+configuration_n

space_volume = [1, 1, 1, 2, 4, 9, 20, 48, 115]
for n in range(9, 100):
    all_loops_result = 0
    for i in range(1, 12):
        globals()['x' + str(i)] = n - 1
    for m_0 in range(1, 12):
        print('recursive result for m={}'.format(m_0))
        residue = n - 1
        x_previous = n - 1
        one_loop_result=0
        loop_rec(residue, x_previous, m_0)
        print('one_loop_result:{}'.format(one_loop_result))
        all_loops_result=all_loops_result+one_loop_result
    print('all_loops_result:{}'.format(all_loops_result))
    space_volume.append(all_loops_result)
f=open('/data/results/space_volume.txt', 'wb')
pickle.dump(space_volume,f)
f.close()

