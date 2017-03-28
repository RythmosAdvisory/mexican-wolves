from pack import Pack, generate_pack
from random import normalvariate
from math import ceil
import matplotlib.pyplot as plt
import statistics


def main():
    # Pack sizes for gray wolves range from about 2 to 8 members [4]
    packs = [generate_pack(ceil(normalvariate(5,3))) for i in range(0,3)]

    sim_100y_500p = run_sim(100, 500, packs.copy())
    sim_100y_50p = run_sim(100, 50, packs.copy())
    
    print('100 years, 500 max population, final pop')
    print(histogram_of_allele_variance_total(sim_100y_500p[-1]['packs']))
    print('100 years, 500 max population, first pop')
    print(histogram_of_allele_variance_total(sim_100y_500p[0]['packs']))
    print('100 years, 50 max population, final pop')
    print(histogram_of_allele_variance_total(sim_100y_50p[-1]['packs']))
    print('100 years, 500 max population, first pop')
    print(histogram_of_allele_variance_total(sim_100y_50p[0]['packs']))
    
    hist_100y_500p_last = histogram_of_allele_total(sim_100y_500p[-1]['packs'])
    hist_100y_500p_first = histogram_of_allele_total(sim_100y_500p[0]['packs'])
 
    hist_100y_50p_last = histogram_of_allele_total(sim_100y_50p[-1]['packs'])
    hist_100y_50p_first = histogram_of_allele_total(sim_100y_50p[0]['packs'])
    
    fig1 = plt.figure(1)
    fig1.suptitle('Histogram of genetic variation in gene "a" for max population 500 over 100 years')
    ax = fig1.add_subplot(211)
    ax.hist(hist_100y_500p_first['a'])
    ax.set_title('first generation')
    ax.set_xlabel('allele')
    ax.set_ylabel('number of wolves')
    ax.set_xlim([0,5])
    ax = fig1.add_subplot(212)
    ax.hist(hist_100y_500p_last['a'])
    ax.set_title('last generation')
    ax.set_xlabel('allele')
    ax.set_ylabel('number of wolves')
    ax.set_xlim([0,5])
   
    fig2 = plt.figure(2)
    fig2.suptitle('Histogram of genetic variation in gene "a" for max population 50 over 100 years')
    ax = fig2.add_subplot(211)
    ax.hist(hist_100y_50p_first['a'])
    ax.set_title('first generation')
    ax.set_xlabel('allele')
    ax.set_ylabel('number of wolves')
    ax.set_xlim([0,5])
    ax = fig2.add_subplot(212)
    ax.hist(hist_100y_50p_last['a'])
    ax.set_title('last generation')
    ax.set_xlabel('allele')
    ax.set_ylabel('number of wolves')
    ax.set_xlim([0,5])
 
    plt.show()


def run_sim(max_years, max_population, packs=None):
    # start simulation at year 0
    year = 0
    if packs is None:
        # Pack sizes for gray wolves range from about 2 to 8 members [4]
        packs = [generate_pack(ceil(normalvariate(5,3))) for i in range(0,3)]
    time_data = [{
        'year':0,
        'packs':packs,
        'stats':{
            'num_packs':len(packs),
            'wolf_pop':wolf_population(packs),
            'avg_genetic_var':wolf_pop_genetic_variance(packs)}
        }]
    for i in range(0,max_years):
        year += 1;
        next_iter_packs = []
        for p in packs:
            p.age()
            if wolf_population(packs) < max_population:
                p.mate()
            p.deaths()
            if len(p.wolves) > 8:
                next_iter_packs.extend(split_pack(p))
            elif len(p.wolves) > 0:
                next_iter_packs.append(p)
        packs = next_iter_packs
        time_data.append({
            'year':year,
            'packs':packs,
            'stats':{
                'num_packs':len(packs),
                'wolf_pop':wolf_population(packs),
                'avg_genetic_var':wolf_pop_genetic_variance(packs)}
        })

    return time_data


def plot_time_stats(time_data):
    years = [d['year'] for d in time_data]
    num_packs = [d['stats']['num_packs'] for d in time_data]
    wolf_pop = [d['stats']['wolf_pop'] for d in time_data]
    avg_genetic_var = [d['stats']['avg_genetic_var'] for d in time_data]

    plt.figure(1)
    plt.plot(years, num_packs, 'ro')
    plt.ylabel('num packs')
    plt.xlabel('years')

    plt.figure(2)
    plt.plot(years, wolf_pop, 'ro')
    plt.ylabel('wolf population')
    plt.xlabel('years')

    plt.figure(3)
    plt.plot(years, avg_genetic_var, 'ro')
    plt.ylabel('average genetic variance of packs')
    plt.xlabel('years')

    plt.show()


def split_pack(p):
    len_new_pack = ceil(len(p.wolves)/2)
    new_packs = [Pack(p.wolves[0:len_new_pack]), Pack(p.wolves[len_new_pack:len(p.wolves)])]
    return new_packs


def wolf_population(packs):
    return sum(len(p.wolves) for p in packs)


def wolf_pop_genetic_variance(packs):
    return sum(p.average_genetic_variance() for p in packs)/len(packs)


def wolf_pop_genetic_std_dev(packs):
    return sum(p.average_genetic_std_dev() for p in packs)/len(packs)


def ages_lsp(p):
    alsp = [{'age': p.wolves[i].age, 'lsp': p.wolves[i].lifespan} for i in range(0,len(p.wolves))] 
    return alsp


def histogram_of_allele_variance_total(packs):
    histogram = histogram_of_allele_total(packs)
    for k in histogram.keys():
        histogram[k] = statistics.pvariance(histogram[k])
    return histogram
     

def histogram_of_allele_total(packs):
    histogram = {'a':[], 'b':[], 'c':[], 'd':[], 'e':[], 'f':[]}
    for p in packs:
        merge_histograms(histogram, p.histogram_of_allele())
    return histogram

def merge_histograms(a, b):
    for k in a.keys():
        a[k].extend(b[k])


if __name__=='__main__':
    main()

