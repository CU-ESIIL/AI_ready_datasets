"""V3 public renderer, transparent phrase baseline and shared-controller protocol."""
import json
from time import perf_counter_ns
from .agent_render import SYSTEM, public_data
from .agent_environment import Dispatcher
from .agent_providers import ProviderReply
from .pilot_contracts import PilotAction, PilotArguments, PilotQuery, OPS
from .pilot_operations import CONTRACTS
from ..contracts import digest


def serialize(initial,history):
    return json.dumps({'system':SYSTEM,'initial':initial,'history':history,'action_schema':PilotAction.model_json_schema()},
      sort_keys=True,separators=(',',':'),allow_nan=False)

PROTOCOL=(PilotAction,PilotArguments,PilotQuery,OPS,serialize)


def render(task,allowed,metadata,stores,aliases,costs):
    q=task.query
    evidence={
      'M0':{'parse':'JSON; null is unavailable, not zero. km2 area and km2/day daily increments. Synthetic observations only.'},
      'M1':{'parse':'JSON; null is unavailable, not zero. km2 area and km2/day daily increments. Synthetic observations only.',
        'meaning':'Completed developmental allocation divides growth by its total, losing absolute scale and native calendar dates. A multi-day endpoint difference is an interval total, not a daily increment. PCA is fitted only on training histories.'},
      'M2':{'parse':'JSON; null is unavailable, not zero. km2 area and km2/day daily increments. Synthetic observations only.',
        'operation_contracts':CONTRACTS,
        'preconditions':'Primary profiles require >=3 consecutive evidenced one-day increments and positive total. Unknown baseline/gap invalidates normalization. Retained source-ID counts support consecutive duration only when primary eligibility is true.',
        'uncertainty':'Synthetic generator values have no real measurement error model. Unknown availability timestamps cannot establish prospective access. Geometric neighbors are not validated ecological analogs.',
        'claims':'Normalized scale is noninvertible. Three retained PCs do not uniquely determine an arbitrary 20-bin profile or its discarded residual; projected distances must not be called full-profile distances. Provenance preserves rights/evidence but cannot approve scientific meaning.'}}
    return {'version':'fire-pilot-prompt-v3','question':task.question,
      'context':{'fire_ids':[aliases[i] for i in q.fire_ids],'requested_date':str(q.date) if q.date else None,
        'interval_start_date':str(q.start_date) if q.start_date else None,'candidate_fire_ids':[aliases[i] for i in q.candidates]},
      'allowed_representations':list(allowed),'operations':{op:{'version':'3','arguments':['fire_ids']+(['date'] if op in {'cumulative','daily_growth','interval_growth','growth_compare'} else [])+(['start_date'] if op in {'interval_growth','growth_compare'} else [])+(['claim'] if op=='assess_claim' else [])+(['candidates'] if op=='neighbor_stability' else [])} for op in OPS},
      'interaction_budget':{'steps':6,'tool_calls':4,'prompt_bytes':48000},
      'data':{r:public_data(q,r,stores[r],aliases) for r in allowed},'metadata':evidence[metadata],
      'representation_formats':{'R0':'dated native observations','R1':'20-bin allocation and retained traits','R2':'three frozen standardized PCs'},
      'workload':{'preparation_paid':task.preparation_paid,'identical_query_count':task.workload_queries,
        'accounting_scope':'Counterfactual first-use or already-prepared artifacts; identical query-result caching available for all views.',
        'measured_costs':costs}}


class PilotDispatcher(Dispatcher):
    def __init__(self,task,allowed,stores,aliases,reverse):
        super().__init__(task.query,allowed,stores,aliases,reverse,query_contract=PilotQuery)
    def call(self,*args):
        public=super().call(*args)
        if args[1]=='neighbor_stability' and public['status']=='value':
            public['value']={k:self.aliases[v] if k.endswith('neighbor') else v for k,v in public['value'].items()}
            self.calls[-1]['public_result']=public
        return public


def parse_goal(text):
    # Explicit phrase baseline, frozen with the protocol, not model understanding.
    lower=text.lower()
    if text.startswith('Development specification: compute '):return text.split('compute ',1)[1].split(' ',1)[0],None
    pairs=[('one-day increment','daily_growth'),('subtract the second','growth_compare'),('interval total','interval_growth'),
      ('ledger closes','cumulative'),('first-ranked neighbor','neighbor_stability'),('l2 allocation mass discrepancy','reconstruction_error'),
      ('l2 residual','reconstruction_error'),('three-axis projections','projected_distance'),('reconstructed three-axis geometry','projected_distance'),
      ('standardized three-axis geometry','pca_distance'),('twenty allocation cells','profile_distance'),
      ('twenty-cell allocation','profile'),('recurrent growth peaks','pulse_count'),('final quarter','late_fraction'),
      ('midpoint','front_fraction'),('first-half mass','front_fraction'),('source’s version','source_evidence')]
    for phrase,op in pairs:
        if phrase in lower:return op,None
    claims=[('ecological analog','ecological_analog'),('uncertainty distribution','measurement_uncertainty'),('measurement uncertainty','measurement_uncertainty'),('operational forecaster','forecast_availability'),('prospective access','forecast_availability'),('absolute burned area','absolute_from_normalized'),('exact twenty','exact_profile_from_pcs'),
      ('one-day intervals','duration_from_sidecar')]
    for phrase,claim in claims:
        if phrase in lower:return 'assess_claim',claim
    return None,None


class PilotMock:
    simulated=True
    def __init__(self,rule=False):
        self.rule=rule;self.name='v3-contract-cost-router' if rule else 'v3-first-view-mock';self.model=self.name
    def invoke(self,prompt,*,parameters):
        start=perf_counter_ns();p=json.loads(prompt);initial=p['initial'];history=p['history']
        results=[x['response'] for x in history if x['kind']=='tool' and x['response'].get('status') in {'value','no_result'}]
        if results:
            result=results[-1]
            action=PilotAction(action='answer',result_id=result['result_id'],evidence_ids=result['evidence_ids'],
              interpretation='approximate' if result['approximate'] else 'exact') if result['status']=='value' else PilotAction(action='abstain',reason='No supported result',interpretation='insufficient')
        else:
            op,claim=parse_goal(initial['question']);context=initial['context'];allowed=initial['allowed_representations']
            # Claim rubric choices in development are not public; abstain instead of
            # consulting hidden task records. Real provider sees only this envelope.
            if op is None or (op=='assess_claim' and claim is None):action=PilotAction(action='abstain',reason='Public phrase baseline cannot resolve this goal',interpretation='unknown')
            else:
                r=allowed[0]
                if self.rule:
                    options=[]
                    for candidate in allowed:
                        native=op in {'cumulative','daily_growth','interval_growth','growth_compare'}
                        full=op in {'front_fraction','late_fraction','profile','profile_distance','pulse_count','reconstruction_error','neighbor_stability'}
                        if native and candidate!='R0' or full and candidate=='R2':continue
                        options.append(candidate)
                    if options:
                        metrics=initial['workload']['measured_costs'];n=initial['workload']['identical_query_count'];paid=initial['workload']['preparation_paid']
                        # No hidden sufficiency/reference outcomes in this public timing table.
                        r=min(options,key=lambda x:(0 if paid else metrics[x]['preparation_ns'])+metrics[x]['cold_ns']+(n-1)*metrics[x]['warm_ns'])
                fields={'fire_ids':context['fire_ids']}
                if op in {'cumulative','daily_growth','interval_growth','growth_compare'}:fields['date']=context['requested_date']
                if op in {'interval_growth','growth_compare'}:fields['start_date']=context['interval_start_date']
                if op=='neighbor_stability':fields['candidates']=context['candidate_fire_ids']
                if op=='assess_claim':fields['claim']=claim
                action=PilotAction(action='call',representation=r,operation=op,arguments=fields)
        return ProviderReply(action.model_dump_json(),self.name,self.model,'explicit_mock_or_rule_json',perf_counter_ns()-start)
