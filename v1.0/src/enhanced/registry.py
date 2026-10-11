"""Version 2 registry. Stable sklearn implementations behind a uniform fit/predict API."""
from dataclasses import dataclass
from types import MappingProxyType
import importlib.metadata
import math
import warnings
import numpy as np
from sklearn.linear_model import LinearRegression,Ridge
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from ..registries import MODEL_REGISTRY as BASELINES,CapabilityRequest
from .specification import PARAMETERS


@dataclass(frozen=True)
class Capability:
 name:str
 implementation:str
 kind:str
 targets:tuple
 scaled:bool=False


REGISTRY_V2=MappingProxyType({
 'naive':Capability('naive','preserved src.registries.naive','baseline',('level',)),
 'seasonal_naive':Capability('seasonal_naive','preserved src.registries.seasonal_naive','baseline',('level',)),
 'linear':Capability('linear','sklearn.linear_model.LinearRegression','supervised',('level','cumulative_log_change'),True),
 'ridge':Capability('ridge','sklearn.linear_model.Ridge(solver=svd)','supervised',('level','cumulative_log_change'),True),
 'autoregression':Capability('autoregression','sklearn.linear_model.LinearRegression on lagged log returns, recursive AR(p)','autoregressive',('monthly_log_return',)),
 'random_forest':Capability('random_forest','sklearn.ensemble.RandomForestRegressor','supervised',('level','cumulative_log_change')),
 'gradient_boosting':Capability('gradient_boosting','sklearn.ensemble.GradientBoostingRegressor','supervised',('level','cumulative_log_change'))})


def require(name):
 if name not in REGISTRY_V2:raise CapabilityRequest('Unregistered Stage 6 model: '+name)
 return REGISTRY_V2[name]


def registry_record():
 from dataclasses import asdict
 return {'version':2,'baseline_registry_unchanged':True,'families':{n:{**asdict(c),'parameter_space':PARAMETERS[n],
    'compatible_feature_families':['history','trend','state','policy','cross_category'] if c.kind=='supervised' else ['target_history'],
    'seed':42 if n in {'random_forest','gradient_boosting'} else None} for n,c in REGISTRY_V2.items()},
  'unavailable':{'SARIMA':'statsmodels not installed; no comparable installed implementation has been established; no downloads/installations.'},
  'dependencies':{n:importlib.metadata.version(n) for n in ['numpy','scipy','scikit-learn']}}


class Fitted:
 def __init__(self,cap,params,estimator,scaler,metadata):
  self.cap,self.params,self.estimator,self.scaler,self.metadata=cap,params,estimator,scaler,metadata
 def predict(self,X):
  a=np.asarray(X,dtype=float)
  if self.cap.kind=='baseline':
   return np.asarray(self.estimator,dtype=float)
  if a.ndim!=2 or not np.isfinite(a).all():raise ValueError('Invalid prediction design matrix.')
  if self.scaler is not None:a=self.scaler.transform(a)
  out=np.asarray(self.estimator.predict(a),dtype=float)
  if not np.isfinite(out).all():raise ValueError('Nonfinite registered predictions.')
  return out


def fit(name,X,y,params,target,feature_names):
 cap=require(name)
 if params not in PARAMETERS[name]:raise PermissionError('Hyperparameters outside predeclared bounded registry space.')
 if target not in cap.targets:raise PermissionError('Unregistered target/model combination.')
 if cap.kind=='baseline':
  vals=np.asarray(y,dtype=float)
  if len(vals)<12 or not np.isfinite(vals).all() or np.any(vals<=0):raise ValueError('Invalid baseline history.')
  return Fitted(cap,params,BASELINES[name].function(vals.tolist(),13),None,{'parameters_fitted':0,'scaler':None})
 a=np.asarray(X,dtype=float);b=np.asarray(y,dtype=float)
 if a.ndim!=2 or b.ndim!=1 or len(a)!=len(b) or len(a)<90 or not np.isfinite(a).all() or not np.isfinite(b).all():
  raise ValueError('Registered fit requires >=90 finite supervised examples, without imputation.')
 scaler=StandardScaler().fit(a) if cap.scaled else None
 aa=scaler.transform(a) if scaler is not None else a
 if name in {'linear','autoregression'}:model=LinearRegression()
 elif name=='ridge':model=Ridge(**params,solver='svd')
 elif name=='random_forest':model=RandomForestRegressor(**params,random_state=42,n_jobs=1)
 else:model=GradientBoostingRegressor(**params,random_state=42,loss='squared_error')
 with warnings.catch_warnings(record=True) as warned:
  warnings.simplefilter('always');model.fit(aa,b)
 meta={'training_rows':len(a),'feature_names':feature_names,'parameters':params,'warnings':[str(w.message) for w in warned],
   'scaler':None if scaler is None else {'mean':scaler.mean_.tolist(),'scale':scaler.scale_.tolist(),'n_samples_seen':int(scaler.n_samples_seen_)},
   'coefficients':model.coef_.tolist() if hasattr(model,'coef_') else None,
   'intercept':float(model.intercept_) if hasattr(model,'intercept_') else None,
   'feature_importances':model.feature_importances_.tolist() if hasattr(model,'feature_importances_') else None,
   'seed':42 if name in {'random_forest','gradient_boosting'} else None,
   'conditioning':float(np.linalg.cond(aa)) if cap.kind in {'supervised','autoregressive'} and name in {'linear','ridge','autoregression'} else None}
 return Fitted(cap,params,model,scaler,meta)
