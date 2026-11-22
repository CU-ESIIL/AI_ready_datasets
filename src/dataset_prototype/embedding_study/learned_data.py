"""Synthetic observation controls and prefix-only, target-free preprocessing."""
from datetime import date,datetime,timedelta,timezone
import numpy as np
from ..contracts import digest
from .learned_contracts import PrefixInput,PrefixOutcome

RECIPE='prefix-observed-day-v1; no full-history VASE normalization'


def generate(config):
    rng=np.random.default_rng(config.generator_seed);records=[];histories=[]
    for split,count,year in [('train',config.train_fires,2021),('validation',config.validation_fires,2022),('test',config.test_fires,2023)]:
        for i in range(count):
            identifier=f'synthetic-{split}-{i:04d}';scale=rng.uniform(.5,2.);state=rng.uniform(.2,2.);values=[]
            mode=i%3
            for day in range(14):
                # Fixed stochastic controls, not ecological labels or physical mechanisms.
                baseline=.45+.2*np.sin(.7*day+i)
                loggrowth=.65*state+baseline+(.2*state*state/(1+state) if mode==1 else 0)+rng.normal(0,.16)
                if mode==2 and day%5==2:loggrowth+=.6
                state=max(0.,min(4.,loggrowth));values.append(float(scale*np.expm1(state)))
            first=date(year,6,1)+timedelta(days=i%20)
            histories.append({'fire_id':identifier,'split':split,'synthetic_year':year,
              'synthetic_region':'B' if split=='test' and i%2 else 'A','growth_km2_day':values,
              'first_date':str(first),'source_version':'synthetic-growth-control-v1','rights':'CC0-1.0 project-authored synthetic observations'})
            for depth in config.depths:
                dates=[first+timedelta(days=d) for d in range(depth)]
                availability=[datetime.combine(d+timedelta(days=1),datetime.min.time(),tzinfo=timezone.utc) for d in dates]
                prefix=PrefixInput(fire_id=identifier,source_version='synthetic-growth-control-v1',synthetic=True,
                  source_observation_ids=tuple(identifier+f':D{j}' for j in range(depth)),dates=dates,available_at=availability,
                  issued_at=availability[-1],growth_km2_day=values[:depth])
                target_day=first+timedelta(days=depth)
                outcome=PrefixOutcome(fire_id=identifier,date=target_day,observation_id=identifier+f':D{depth}',
                  growth_km2_day=values[depth],available_at=datetime.combine(target_day+timedelta(days=1),datetime.min.time(),tzinfo=timezone.utc))
                records.append({'split':split,'synthetic_year':year,'synthetic_region':histories[-1]['synthetic_region'],
                  'prefix':prefix,'outcome':outcome})
    return histories,records


def validate_pair(prefix,outcome):
    if outcome.fire_id!=prefix.fire_id or (outcome.date-prefix.dates[-1]).days!=1 or outcome.observation_id in prefix.source_observation_ids or outcome.available_at<=prefix.issued_at:
        raise ValueError('independent next-calendar-day outcome required')


def raw_tensor(prefixes):
    if not all(isinstance(p,PrefixInput) for p in prefixes):raise TypeError('validated prefix objects only')
    result=np.zeros((len(prefixes),12,4))
    for i,p in enumerate(prefixes):
        n=len(p.dates);g=np.array(p.growth_km2_day)
        result[i,-n:,0]=np.log1p(g);result[i,-n:,1]=np.log1p(np.cumsum(g))
        result[i,-n:,2]=1.;result[i,-n:,3]=np.log1p(n)
    return result


def interpretable(prefixes):
    # Prefix-local descriptors only. Observed-prefix early mass uses absolute area; no undefined zero-total normalization.
    rows=[]
    for p in prefixes:
        g=np.array(p.growth_km2_day);n=len(g);total=g.sum();x=np.log1p(g)
        rows.append([x[-1],float(x.mean()),float(x.std()),np.log1p(total),x[-1]-x[-2],
          float(np.mean(g==0)),np.log1p(n),float(np.log1p(g[:n//2].sum())),float(x[-3:].mean())])
    return np.asarray(rows)


class PrefixPreprocessor:
    def fit(self,prefixes):
        x=raw_tensor(prefixes);mask=x[:,:,2]==1
        self.mean=np.zeros(4);self.scale=np.ones(4)
        for c in (0,1,3):
            self.mean[c]=x[:,:,c][mask].mean();self.scale[c]=max(x[:,:,c][mask].std(),1e-8)
        self.training_ids=tuple(sorted({p.fire_id for p in prefixes}));return self
    def transform(self,prefixes):
        x=raw_tensor(prefixes);mask=x[:,:,2].copy()
        x=(x-self.mean)/self.scale;x*=mask[:,:,None];return x
    def state(self):return {'recipe':RECIPE,'mean':self.mean.tolist(),'scale':self.scale.tolist(),'training_ids':list(self.training_ids)}


def cache_identity(prefix,checkpoint_digest,preprocessing):
    return digest({'prefix':prefix.model_dump(mode='json'),'checkpoint':checkpoint_digest,'preprocessing':preprocessing,'recipe':RECIPE})
