"""Reproduce manually reviewed development episode annotations; no model calls."""
import json
from pathlib import Path
from property_eval.prefix import HEADER,load_prefix
from property_eval.checkpoints import TARGET_EVENTS
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('/Users/ryan/code/HackatonPublicCases')
# Authored endpoints: stop before changed knowledge or a fresh follow-up trigger.
ENDS=[5,8,5,7,4,5,6,5,5,7,5,7,7,7,5,4,5,4,5,4,4,4,4,4,4,7,3,5,9,4,6,4,6,7,4,4,5,7,4,6]
BOUNDARIES={1:(6,7),2:(9,),3:(6,7),4:(8,9),5:(5,),6:(6,),7:(7,8),8:(6,),9:(6,),10:(8,),11:(6,),12:(8,),13:(8,),14:(8,9),15:(6,7),16:(5,),17:(6,7),18:(5,),19:(6,),20:(5,6),21:(5,6),22:(4,),23:(5,6),24:(5,6),25:(5,6),26:(8,9),27:(4,),28:(6,7),29:(10,),30:(5,),31:(7,),32:(5,6),33:(7,8),34:(8,),35:(4,),36:(5,6),37:(6,7),38:(8,9),39:(5,6),40:(7,8)}
# event(s), intent, observational materiality, independently authored description.
M='material';A='auxiliary';W='workflow';U='unassessable'
ACTS={
1:[([4],'request_clarification',M,'Ask landlord how to respond to communal gardening request.')],
2:[([5,8],'instruct_provider',M,'Send blockage scope and instruct provider to coordinate access, complete work or quote if required; quoted work awaits approval.'),([7],'notify',A,'Tell tenant provider will arrange attendance.')],
3:[([4],'instruct_provider',M,'Request cleaning/removal/carpet estimate with checkout report.'),([3],'notify',A,'Direct provider to substantive email.')],
4:[([6],'instruct_provider',M,'Request checkout-based cleaning quote with inspection report.'),([5],'notify',A,'Direct provider to substantive email.')],
5:[([4],'instruct_provider',M,'Request cleaning and bedroom carpet estimate after vacancy.')],
6:[([4],'notify',A,'Tell tenant provider will arrange quotation, followed by landlord approval.'),([5],'instruct_provider',M,'Ask provider to coordinate access and quote for checkout works; do not proceed with quoted work before approval.')],
7:[([5],'instruct_provider',M,'Request quote for spotlights and ceiling tile with checkout report.'),([4],'notify',A,'Direct provider to substantive email.')],
8:[([3],'instruct_provider',M,'Request multi-item checkout works estimate with report.'),([4],'notify',A,'Direct provider to substantive email.')],
9:[([3,4],'request_clarification',M,'Ask tenant whether garden maintenance is complete and request photos.')],
10:[([6],'request_clarification',M,'Request clear photo of solar panel readings.')],
11:[([4],'request_approval',M,'Ask landlord permission to send dishwasher engineer.')],
12:[([5,6],'provide_guidance',M,'Send dishwasher obstruction checks and request response if door still fails.')],
13:[([2],'notify',A,'Tell landlord an appliance engineer will be sent.'),([5],'notify',A,'Tell tenant quotation visit will be arranged.'),([6],'instruct_provider',M,'Ask provider to arrange quotation visit and supply evidence and completion estimate.'),([7],'notify',A,'Direct provider to substantive email.')],
14:[([5],'notify',A,'Report fridge freezer fitted.'),([5],'request_approval',M,'Ask landlord permission for front-door inspection.'),([6],'notify',A,'Acknowledge tenant report and pending landlord contact.')],
15:[([3],'request_approval',M,'Ask landlord permission to instruct door contractor.'),([4],'notify',A,'Tell tenant landlord instructions are pending.'),([4],'provide_guidance',M,'Ask tenant to report worsening operation or security concerns immediately.')],
16:[([3],'request_approval',M,'Ask landlord whether agency should send contractor or landlord will arrange.')],
17:[([3],'notify',A,'Acknowledge extractor issue and intended landlord contact.'),([4],'request_approval',M,'Ask landlord to choose own or agency contractor.')],
18:[([4],'notify',A,'Tell tenant gardener is on leave and will be booked after return.')],
19:[([3],'request_clarification',M,'Ask landlord plans and desired response to garden works request.'),([4],'notify',A,'Acknowledge tenant request and pending landlord response.')],
20:[([2,3],'notify',M,'Confirm inspection date/window, photography and management-key access; email repeats schedule.')],
21:[([3],'request_approval',M,'Ask landlord permission to arrange broken-key works.')],
22:[([4],'propose_booking',M,'Contact tenant to arrange contractor attendance; exact initial proposal cannot be separated reliably from tenant agreement in summary.')],
23:[([3],'request_approval',M,'Ask landlord permission for balcony lock attendance.'),([4],'notify',A,'Prompt landlord to check approval email; immediate channel cue, not evidence of elapsed timeout.')],
24:[([3],'provide_guidance',M,'Suggest oven dial/temperature settings and send manual.')],
25:[([3],'request_approval',M,'Ask landlord whether agency or own contractor should attend oven.')],
26:[([4],'request_approval',M,'Ask landlord permission to send named appliance provider.'),([6],'notify',A,'Tell tenant approval has been requested.')],
27:[([2],'provide_guidance',M,'Recommend drain cleaner/plunger and describe claimed tenant responsibility and conditional costs.'),([2],'request_clarification',M,'Ask how tenant wishes to proceed, including arranging plumber.')],
28:[([3],'request_approval',M,'Ask landlord whether agency or own contractor should address loose pipe.'),([4],'notify',A,'Tell tenant permission has been requested.')],
29:[([4],'notify',A,'Tell tenant provider will arrange quotation.'),([5],'instruct_provider',M,'Ask provider to arrange basin work or quote; quoted work awaits approval.'),([6],'notify',A,'Direct provider to substantive email.'),([7],'request_clarification',M,'Ask tenant how hand basin became cracked.')],
30:[([4],'notify',M,'Tell landlord plumbing job has been raised with Riverside Works.')],
31:[([5],'notify',A,'Tell tenant provider will arrange attendance.'),([6],'instruct_provider',M,'Ask provider to arrange cistern attendance or quote; quoted work awaits approval.')],
32:[([3],'request_approval',M,'Ask landlord whether agency or own contractor should address flusher.')],
33:[([3],'request_approval',M,'Ask landlord whether agency or own contractor should address bathroom tap.'),([4],'notify',A,'Tell tenant permission has been requested.')],
34:[([6],'notify',A,'Tell tenant provider will arrange shower attendance.'),([7],'instruct_provider',M,'Ask provider to coordinate shower works or quote; quoted work awaits approval.')],
35:[([4],'unknown',U,'Call discusses shower and other maintenance costs; summary does not attribute requests or responses to speakers.')],
36:[([3],'request_approval',M,'Ask landlord permission for shower-knob repair attendance.')],
37:[([3],'request_approval',M,'Ask landlord whether landlord or agency should arrange shower repair.'),([4],'request_clarification',M,'Request photos showing damaged shower cable and leak.')],
38:[([4,5],'request_approval',M,'Seek approval for tenant-owned replacement and landlord removal cost; repeated call/email have conflicting property addresses.'),([6],'notify',A,'Tell tenant landlord response is pending.')],
39:[([3],'request_clarification',M,'Ask tenant whether contents are striking machine sides; describe conditional engineer attendance.')],
40:[([4],'request_approval',M,'Ask landlord preferred washing-machine inspection/replacement approach and attendance permission.'),([5],'notify',A,'Tell tenant landlord direction is pending.')],
}
SPECIAL={
5:('unknown_internal_record','Next-day hold has unavailable text; cannot tell whether new evidence or administrative continuation. Conservatively exclude it.','uncertain'),
6:('timer_trigger','Next-day appointment reminder is a new follow-up trigger; timer inferred from reminder and elapsed day, not explicitly logged.','probable'),
8:('unlogged_new_information','Landlord email now encloses an estimate not previously logged as received. Its availability is new knowledge; do not include this later approval request.','probable'),
9:('followup_and_external_response','Five-day-later check-in call includes new tenant explanation; elapsed follow-up trigger is not explicitly logged.','probable'),
10:('mixed_call_new_information','Later call records promise to send readings; fresh interaction and missing speaker detail.','probable'),
11:('timer_trigger','Explicit no-response-after-three-days update.','clear'),
12:('new_internal_evidence','Note008 says landlord already agreed GS attendance. Whether pre-existing but late-recorded is unknown; it was unavailable at prefix4.','uncertain'),
13:('external_observation','Provider call encounters voicemail; new contact outcome.','clear'),
16:('timer_trigger','Explicit no-response-after-three-days update.','clear'),
18:('approval_state_or_new_evidence','Approval-confirmed update could be agency workflow mutation or recording previously unseen authority. Prefix explicitly says approval needed. Conservative boundary; alternative continuation006–008 separately retained.','uncertain'),
19:('timer_trigger','Explicit no-response-after-three-days update.','clear'),
22:('within_call_external_response','Tenant agreement inside call004 is new information. Initial proposal is partially inferable; confirmation and downstream005–008 depend on exchange, not prefix3 alone. No verbatim turn boundaries available.','uncertain'),
27:('timer_trigger','Eleven-day-later nonresponse follow-up asks result and announces24h closure; timer inferred, no explicit timer event.','probable'),
30:('approval_state_or_new_evidence','Approval-confirmed update could be workflow mutation or unseen authority. No explicit approval in prefix3; conservatively stop and retain006–008 as alternative continuation.','uncertain'),
34:('timer_trigger','Next-day appointment reminder is fresh follow-up trigger inferred from wording and elapsed time.','probable'),
35:('within_call_external_response','Mixed call summary004 cannot identify agency initiation vs landlord response; subsequent005–007 may depend on newly agreed landlord plan. Do not treat that plan as prefix knowledge.','uncertain'),
}
LIMITS={10:'Solar topic is absent from supplied prefix; episode grouping cannot make that content predictable.',12:'Prefix explicitly doubts whether door report concerns dishwasher; historical troubleshooting is observed choice, not proof issue linkage resolved.',13:'Engineer selection and authority are not established by the minimal prefix.',18:'Gardener leave and approval basis are absent from prefix.',20:'Exact inspection date/access details are not fully established by minimal prefix; simultaneous internal visit time is not proof prior permission.',22:'Timing in summary and logged timestamps is inconsistent; no executable appointment time can be inferred safely.',24:'Manual content is unavailable; specific settings are not supported by visible prefix.',27:'Tenancy responsibility and cost rules are asserted by historical email, not verified policy.',29:'Cracked-basin detail may rely on unseen attachment; do not make exact crack knowledge a mandatory prediction.',30:'Provider labels differ in alternative continuation; authority provenance is absent.',35:'No assessable pre-response intent beyond a maintenance discussion; later plan cannot repair missing speaker turns.',38:'Call and email have incompatible property address labels; party roles remain usable, but exact property binding is unresolved.'}
def main():
 episodes=[]
 for n in range(1,41):
  case=f'{n:03}'; path=SOURCE/'Property Management'/case/'history.md';raw=path.read_text(); heads=list(HEADER.finditer(raw)); events=load_prefix(SOURCE,case,len(heads)).events;start=TARGET_EVENTS[n-1];end=ENDS[n-1];cutoff=start-1
  def citation(num):
   h=heads[num-1];stop=heads[num].start() if num<len(heads) else len(raw);body=events[num-1].text.split('\n\n',1)[1];pos=raw.index(body,h.end(),stop)
   return {'event_id':f'{num:03}','source_path':str(path.relative_to(SOURCE)),'quote':body,'char_start':pos,'char_end':pos+len(body),'line_start':raw.count('\n',0,pos)+1,'line_end':raw.count('\n',0,pos+len(body))+1,'offset_basis':'zero-based Unicode codepoints in complete history.md; end exclusive'}
  actions=[];used=set()
  for nums,intent,materiality,summary in ACTS[n]:
   used.update(nums);actions.append({'id':f'{case}-a{len(actions)+1:02}','intent':intent,'summary':summary,'materiality':materiality,'source_citations':[citation(i) for i in nums],'deduplication':'Equivalent communication effects combined; individual source wording retained.' if len(nums)>1 else None,'earliest_knowledge':{'cutoff':None,'prediction_cutoff':cutoff,'status':'earliest_factual_availability_not_established','note':'Action belongs before next observed evidence boundary; membership does not prove all factual slots were known at prefix.'}})
  for i in range(start,end+1):
   if i in used:continue
   e=events[i-1];intent='assign_provider' if 'Maintenance provider assigned' in e.text else 'change_workflow' if 'Changed original task description' in e.text else 'record_evidence' if e.channel=='Note' else 'change_workflow';body=e.text.split('\n\n',1)[1]
   # Consecutive equivalent workflow writes are one observed effect.
   duplicate=next((a for a in actions if a['intent']==intent and a['summary']==body),None)
   if duplicate:duplicate['source_citations'].append(citation(i));duplicate['deduplication']='Duplicate workflow state effect.';continue
   actions.append({'id':f'{case}-a{len(actions)+1:02}','intent':intent,'summary':body,'materiality':W,'source_citations':[citation(i)],'earliest_knowledge':{'cutoff':cutoff,'status':'observed_agency_effect_not_new_external_fact','note':'Administrative transition is recorded; no independent truth or authorization inferred.'}})
  kind,reason,confidence=SPECIAL.get(n,('external_reply','Incoming communication is new information; immediately preceding review/display update is included in boundary cluster, not treated as independent domain evidence.','clear'))
  bnums=list(BOUNDARIES[n]);tailend=min(len(events),max(max(bnums)+2,{18:9,22:9,30:9,35:9}.get(n,0)))
  partial=[]
  for a in actions:
   if a['materiality']=='workflow' and ('Waiting' in a['summary'] or 'waiting' in a['summary'] or 'Hold for quote' in a['summary']):
    preceding=[x for x in actions if x['materiality']=='material' and max(int(c['event_id']) for c in x['source_citations'])<int(a['source_citations'][0]['event_id'])]
    for x in preceding:
     recipients={events[int(c['event_id'])-1].recipient.lower() for c in x['source_citations']}
     target='landlord' if 'landlord' in a['summary'].lower() else 'tenant' if 'tenant' in a['summary'].lower() else 'contractor' if 'provider' in a['summary'].lower() or 'quote' in a['summary'].lower() else None
     if target not in recipients:continue
     partial.append({'before':x['id'],'after':a['id'],'basis':'Recorded outbound request precedes waiting for its response; ordering within simultaneous communications is unspecified.'})
  for action in actions:
   action['execution_semantics']='Observed communication or recorded administrative effect; requested repair/visit/approval is not evidence that work executed or approval granted.'
   action['observed_at_event']=action['source_citations'][0]['event_id']
   if 'Changed original task description' in action['summary']:action['workflow_operation']='revise_description'
  if n==22:
   actions[0]['source_citations'][0]['quote']='The customer was contacted by Miles from Northbridge Lettings to address an issue with their door lock.'
   c=actions[0]['source_citations'][0];c['char_end']=c['char_start']+len(c['quote']);c['line_end']=c['line_start'];actions[0]['earliest_knowledge']['status']='only_initial_contact_observable; proposal_slots_not_separable'
  if n==35:actions[0]['earliest_knowledge']['status']='cannot_separate_pre_response_agency_intent'
  episodes.append({'checkpoint_id':f'{case}-at-{cutoff:03}','case_id':case,'cutoff':cutoff,'included_event_ids':[f'{i:03}' for i in range(start,end+1)],'actions':actions,'boundary':{'event_ids':[f'{i:03}' for i in bnums],'kind':kind,'reason':reason,'confidence':confidence,'citations':[citation(i) for i in bnums]},'partial_order':partial,'source_tail':[{'event_id':f'{i:03}','timestamp':events[i-1].timestamp,'channel':events[i-1].channel,'sender':events[i-1].sender,'recipient':events[i-1].recipient,'citation':citation(i),'role':'episode' if i<=end else 'boundary_or_later_review_only'} for i in range(start,tailend+1)],'alternative_continuation_event_ids':{'018':['006','007','008'],'030':['006','007','008'],'022':['005','006','007','008'],'035':['005','006','007']}.get(case,[]),'limits':[LIMITS[n]] if n in LIMITS else [],'target_completeness':'partial_mixed_call' if n in (22,35) else 'boundary_ambiguous' if confidence=='uncertain' else 'observed_bundle','normative_required_actions':None})
 doc={'version':'decision-episodes-v1','author':'implementing assistant; independent source review','review_date':'2026-10-10','scope':'Property Management001–040 development checkpoints, unchanged prefixes;041–050 excluded','visibility':'evaluation_only','old_score_status':'2/40 was model-judged correspondence against first-message targets, not a valid full decision-episode score. No episode rescore has yet been performed by this author.','identity_assumption':'Contextual landlord, tenant and agency roles are usable identities; no CRM identity lookup requirement.','materiality_semantics':{'material':'Distinct observed operational request, guidance, instruction or substantive arrangement. Not a normative requirement.','auxiliary':'Acknowledgment, status notification or channel cue supporting operation; separately report omission.','workflow':'Recorded administrative effect; not new external evidence unless content records unseen authority/observation.','unassessable':'Source insufficient to identify agency act.'},'episodes':episodes}
 doc['summary']={'checkpoints':len(episodes),'actions':sum(len(e['actions']) for e in episodes),'multi_event_episodes':sum(len(e['included_event_ids'])>1 for e in episodes),'uncertain_boundary_cases':[e['case_id'] for e in episodes if e['boundary']['confidence']=='uncertain'],'partial_mixed_call_cases':['022','035'],'multi_material_action_cases':[e['case_id'] for e in episodes if sum(a['materiality']=='material' for a in e['actions'])>1]}
 out=ROOT/'annotations/decision-episodes-v1.json';out.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n');print(json.dumps(doc['summary']))
if __name__=='__main__':main()
