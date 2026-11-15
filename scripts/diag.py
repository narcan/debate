import json,sys,collections
for p in sys.argv[1:]:
    r=[json.loads(l) for l in open(p)]; r=[x for x in r if not x.get('error')]
    n=len(r); 
    if not n: continue
    A=lambda xs:(sum(1 for x in xs if x['judge_correct'])/len(xs)) if xs else float('nan')
    print(p.split('/')[-1],n,'verdictA %.2f'%(sum(x['verdict']=='A' for x in r)/n),'invalid',sum(x['verdict'] is None for x in r),
      'v0(assigned correct) %.3f v1 %.3f'%(A([x for x in r if x['variant']==0]),A([x for x in r if x['variant']==1])),
      'corr=A %.3f corr=B %.3f'%(A([x for x in r if x['correct']=='A']),A([x for x in r if x['correct']=='B'])),
      'cost/deb %.4f'%(sum(x['cost'] for x in r)/n),'calls %.1f'%(sum(x['n_calls'] for x in r)/n),
      'dbt cached/prompt %.2f'%(sum(x.get('debater_cached_tokens',0) for x in r)/max(1,sum(x.get('debater_prompt_tokens',0) for x in r))))
