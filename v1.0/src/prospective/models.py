import hashlib
import numpy as np
from sklearn.linear_model import LinearRegression,Ridge
from sklearn.preprocessing import StandardScaler
from ..enhanced.registry import fit as registered_fit
from .specification import MODELS

def forecast(history,model,horizon=60):
 if model not in MODELS or horizon!=60:raise PermissionError('Outside registered Stage 9 model/horizon')
 y=np.asarray(history,dtype=float)
 if y.ndim!=1 or len(y)<120 or not np.isfinite(y).all() or (y<=0).any():raise ValueError('At least 120 positive training prices required')
 n=len(y);h=np.arange(1,61);meta={'model':model,'training_months':n,'training_price_sha256':hashlib.sha256(y.tobytes()).hexdigest(),'parameters':MODELS[model]['parameters'],'future_policy_used':False}
 if model=='naive':pred=np.full(60,y[-1])
 elif model=='geometric_drift':
  rate=float(np.log(y[-1]/y[0])/(n-1));pred=y[-1]*np.exp(h*rate);meta['monthly_log_drift']=rate
 elif model in {'linear_trend','log_linear_trend','ridge_trend'}:
  x=np.arange(n).reshape(-1,1);future=(n-1+h).reshape(-1,1);scaler=None
  if model=='ridge_trend':
   scaler=StandardScaler().fit(x);x=scaler.transform(x);future=scaler.transform(future);est=Ridge(alpha=12.0,solver='svd')
   meta['scaler']={'mean':scaler.mean_.tolist(),'scale':scaler.scale_.tolist(),'fit_rows':n}
  else:est=LinearRegression()
  target=np.log(y) if model=='log_linear_trend' else y
  est.fit(x,target);pred=est.predict(future)
  if model=='log_linear_trend':
   smear=float(np.mean(np.exp(target-est.predict(x))));pred=np.exp(pred)*smear;meta['training_smearing_factor']=smear
  meta.update(coefficients=est.coef_.tolist(),intercept=float(est.intercept_))
 else:
  lag=MODELS[model]['parameters']['lags'];r=np.diff(np.log(y));ix=np.arange(lag,len(r));x=np.array([r[i-lag:i][::-1] for i in ix])
  fitted=registered_fit('autoregression',x,r[ix],{'lags':lag},'monthly_log_return',[f'log_return_lag{i}' for i in range(1,lag+1)])
  companion=np.zeros((lag,lag));companion[0]=fitted.metadata['coefficients']
  if lag>1:companion[1:,:-1]=np.eye(lag-1)
  meta['AR_spectral_radius']=float(max(abs(np.linalg.eigvals(companion))));meta['fitted']=fitted.metadata
  memory=r.tolist();price=float(y[-1]);pred=[]
  for _ in range(60):
   v=float(fitted.predict(np.array([memory[-lag:][::-1]]))[0]);memory.append(v);price*=float(np.exp(v));pred.append(price)
 pred=np.asarray(pred)
 if not np.isfinite(pred).all() or (pred<=0).any():raise ValueError('Invalid extrapolation; do not clip')
 meta.update(first_month_ratio=float(pred[0]/y[-1]),implied_cagr=float((pred[-1]/y[-1])**.2-1))
 return pred,meta

def extrapolation_ok(meta):
 return -.15<=meta['implied_cagr']<=.25 and .8<=meta['first_month_ratio']<=1.2 and meta.get('AR_spectral_radius',0)<.999
