"""Controlled installed sklearn methods with fixed, validated specifications."""
from types import MappingProxyType
from importlib.metadata import version
import warnings
import numpy as np
from sklearn.cluster import KMeans,AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler,RobustScaler
from .specification import KS,SEEDS

REGISTRY=MappingProxyType({'kmeans':'sklearn.cluster.KMeans','gmm_diag':'sklearn.mixture.GaussianMixture','ward':'sklearn.cluster.AgglomerativeClustering'})
def registry_record():return {'version':'stage8_v1','registered':dict(REGISTRY),'unavailable':{'time_aware':'No existing executable time-aware/regime-switching method; no new installation.'},
 'restricted_variants':{'GMM':'Diagonal covariance only, bounded parameter count; full covariance deferred for 227 observations and correlated features.',
 'hierarchical':'Ward linkage, Euclidean distance, cut at each fixed K=2..6, no visual cut search.'},'dependencies':{n:version(n) for n in ['numpy','scipy','scikit-learn']}}

def fit(method,k,X,seed=42,scaling='standard'):
 if method not in REGISTRY or k not in KS or seed not in SEEDS or scaling not in {'standard','robust'}:raise PermissionError('Unregistered regime configuration.')
 X=np.asarray(X,dtype=float)
 if X.ndim!=2 or X.shape[0]<90 or X.shape[1] not in {4,5,8} or not np.isfinite(X).all():raise ValueError('Invalid regime design matrix.')
 scaler=(StandardScaler() if scaling=='standard' else RobustScaler()).fit(X);Z=scaler.transform(X)
 with warnings.catch_warnings(record=True) as caught:
  warnings.simplefilter('always')
  if method=='kmeans':model=KMeans(n_clusters=k,random_state=seed,n_init=20,algorithm='lloyd');labels=model.fit_predict(Z)
  elif method=='gmm_diag':model=GaussianMixture(n_components=k,covariance_type='diag',random_state=seed,n_init=5,reg_covar=1e-5,max_iter=500);labels=model.fit_predict(Z)
  else:model=AgglomerativeClustering(n_clusters=k,metric='euclidean',linkage='ward',compute_distances=True);labels=model.fit_predict(Z)
 meta={'method':method,'k':k,'seed':seed,'scaling':scaling,'fitted_n':len(X),'scaler_center':(scaler.mean_ if scaling=='standard' else scaler.center_).tolist(),
 'scaler_scale':scaler.scale_.tolist(),'warnings':[str(w.message) for w in caught],'converged':bool(getattr(model,'converged_',True))}
 if method=='kmeans':meta.update(inertia=float(model.inertia_),iterations=int(model.n_iter_),centers_scaled=model.cluster_centers_.tolist())
 if method=='gmm_diag':meta.update(bic=float(model.bic(Z)),aic=float(model.aic(Z)),average_log_likelihood=float(model.score(Z)),iterations=int(model.n_iter_),
     weights=model.weights_.tolist(),means_scaled=model.means_.tolist(),covariances_scaled=model.covariances_.tolist(),posterior=model.predict_proba(Z).tolist())
 if method=='ward':meta.update(linkage='ward',distance='euclidean',cut_rule=f'Fixed cut at {k} groups',children=model.children_.tolist(),distances=model.distances_.tolist())
 return labels,meta,Z
