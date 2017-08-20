''' Inputs:
	psu: ndarray
'''
def subbootstratum(psu, replicates):
	upsu = np.random.choice(np.unique(psu),len(np.unique(psu)), replace=False)
	n = len(upsu)

	return(pd.Series(pd.Categorical.from_codes(np.random.choice(upsu, len(upsu)-1), categories=np.unique(psu))))

def boostratum(psu, popsize, replicates):

def bootweights(strata, psu, replicates=50, fpc=None, fpctype=["population", "fraction", "correction"], compress=True):

''' Inputs:
	strata: pandas Series
	psu: pandas Series
'''
def subbootweights(strata, psu, replicates=50, compress=True):
	psu_to_match = psu[np.unique(psu, return_index=True)[1]]
	index = [l[0] for l in [np.where(psu_to_match == element)[0] for element in psu] if len(l) > 0]
	upsu = psu.unique()
	weights = np.empty(shape=[len(upsu), replicates])
	ustrata = strata[np.unique(psu, return_index=True)[1]]

	for s in np.unique(ustrata):
		stratum = ustrata==s
		npsu = len(np.unique(upsu[np.where(stratum)[0]]))

		weights[np.where(stratum)[0],:] = subbootstratum(upsu[np.where(stratum)[0]], replicates)
	
	rw = None
	if compress:
		rw = {'weights':weights, 'index':index}
		rw['class'] = "repweights_compressed"
	else:
		rw = weights[index,:]

	return({'repweights':rw, 'scale':1/(replicates-1), 'rscales': np.repeat(1,replicates)})
