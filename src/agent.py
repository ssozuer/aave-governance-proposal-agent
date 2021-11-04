from forta_agent import Finding, FindingType, FindingSeverity
from .constants import AAVE_GOVERNANCE_V2_ADDRESS, AAVE_PROPOSAL_EXECUTED_EVENT_ABI

findings_count = 0

def handle_transaction(transaction_event):
    findings = []

    # limiting this agent to emit only 5 findings so that the alert feed is not spammed
    global findings_count
    if findings_count >= 5:
        return findings

    proposal_executed_events = transaction_event.filter_log(AAVE_PROPOSAL_EXECUTED_EVENT_ABI, AAVE_GOVERNANCE_V2_ADDRESS)
    for event in proposal_executed_events:
        proposal_id = event['args']['id']
        proposal_initiator_execution = event['args']['initiatorExecution']

        findings.append(Finding({
            'name': 'Aave Governance Executed Agent',
            'description': f'The governance proposal {proposal_id} executed. Initiator execution: {proposal_initiator_execution}',
            'alert_id': 'AAVE-5',
            'type': FindingType.Info,
            'severity': FindingSeverity.Info
        }))
        findings_count += 1
    return findings

