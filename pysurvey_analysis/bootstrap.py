''' Inputs:
	psu: ndarray
	replicates: integer

	Output:
	pandas DataFrame 
'''
def subbootstratum(psu, replicates):
	upsu = np.random.choice(np.unique(psu),len(np.unique(psu)), replace=False)
	n = len(upsu)

	return(pd.concat([pd.Series(pd.Categorical(np.random.choice(upsu, n-1), categories=np.unique(psu))).value_counts(sort=False) for i in range(replicates)], ignore_index=True, axis=1)*n/(n-1))

def bootstratum(psu, popsize, replicates):
	upsu = np.random.choice(np.unique(psu), len(np.unique(psu)), replace=False).tolist()
	if popsize == None:
			return(pd.concat([pd.Series(pd.Categorical(np.random.choice(upsu, len(upsu)), categories=np.unique(psu))).value_counts(sort=False) for i in range(replicates)], ignore_index=True, axis=1))
	else:
			return(pd.concat([pd.Series(pd.Categorical(np.random.choice(upsu.extend([upsu[i%len(upsu)] for i in range(popsize-len(upsu))]), len(upsu), replace=False), categories=np.unique(psu))).value_counts(sort=False) for i in range(replicates)], ignore_index=True, axis=1))

def bootweights(strata, psu, replicates=50, fpc=None, fpctype=["population", "fraction", "correction"], compress=True):
	psu_to_match = psu[np.unique(psu, return_index=True)[1]]
	index = [l[0] for l in [np.where(psu_to_match == element)[0] for element in psu] if len(l) > 0]
	upsu = np.unique(psu)

	weights = np.empty(shape=[len(upsu), replicates])
	ustrata = strata[np.unique(psu, return_index=True)[1]]
	ufpc = fpc[np.unique(psu, return_index=True)[1]]

	for s in np.unique(ustrata):
		stratum = ustrata==s
		npsu = len(np.unique(upsu[np.where(stratum)[0]]))	

		if fpc == None:
			weights[np.where(stratum)[0],:] = bootstratum(upsu[np.where(stratum)[0]], None, replicates)
		else:
			curr_fpc = ufpc[np.where(stratum)[0]]
			if len(np.unique(curr_fpc)) > 1:
				print("Error: More than one fpc in stratum %d" % (s))
				break
			curr_fpc = curr_fpc[0]
			if fpctype == "population" and curr_fpc < npsu:
				print("Error: Population size smaller than sample size in stratum %d" % (s))
				break
			curr_fpc = dict([("population", curr_fpc), ("fraction", npsu/curr_fpc), ("correction", 1-npsu/curr_fpc)])[fpctype]
			if curr_fpc > (100 * npsu):
				print('Warning message:\nSampling function <1% in stratum, %d, treated as zero' % (s))
			weights[np.where(stratum)[0], :] = bootstratum(upsu[np.where(stratum)[0]], curr_fpc, replicates)

	
	psu_per_strata = scipy.stats.hmean(pd.Series(ustrata).value_counts(sort=False))
	rw = None
	if compress:
		rw = {'weights':weights, 'index':index}
		rw['class'] = 'repweights_compressed'
	else:
		rw = weights[index,:]

	return({'repweights':rw, 'scale':psu_per_strata/((psu_per_strata-1)*(replicates-1)), 'rscales': np.repeat(1,replicates)})

''' Inputs:
	strata: pandas Series or ndarray
	psu: pandas Series or ndarray
'''
def subbootweights(strata, psu, replicates=50, compress=True):
	psu_to_match = psu[np.unique(psu, return_index=True)[1]]
	index = [l[0] for l in [np.where(psu_to_match == element)[0] for element in psu] if len(l) > 0]
	upsu = np.unique(psu)
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
