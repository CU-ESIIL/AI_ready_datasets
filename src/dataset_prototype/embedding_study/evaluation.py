"""Independent answer scoring: correctness, answerability and validity stay separate."""
import math
import numbers


def compare(answer, reference, answer_type):
    if answer_type == 'number':
        if not isinstance(answer,numbers.Real) or isinstance(answer,bool) or not math.isfinite(answer):
            return None
        return abs(float(answer)-float(reference))
    if answer_type == 'profile':
        if not isinstance(answer,list) or len(answer)!=20 or any(not isinstance(v,numbers.Real) or isinstance(v,bool) or not math.isfinite(v) for v in answer):
            return None
        return max(abs(float(x)-float(y)) for x,y in zip(answer,reference))
    if answer_type == 'ids':
        if not isinstance(answer,list) or any(not isinstance(v,str) for v in answer) or len(set(answer))!=len(answer):
            return None
        return 1-len(set(answer)&set(reference))/len(reference)
    return 0. if answer == reference else 1.


def evaluate(task, representation, result, reference, *, execution_error=None):
    sufficient = task.answerable[representation]
    if execution_error:
        status = 'invalid_scientific_operation' if execution_error[0]=='InvalidOperation' else 'execution_failure'
        return {'status':status,'answerable':sufficient,'correctness':None,'numerical_error':None,
            'scientific_validity':'FAIL' if status=='invalid_scientific_operation' else 'NEEDS_EVIDENCE',
            'unsupported_answer':False}
    abstention = result['abstention']
    if abstention:
        return {'status':'incorrect_abstention' if sufficient else 'correct_abstention',
            'answerable':sufficient,'correctness':False if sufficient else None,'numerical_error':None,
            'scientific_validity':'NEEDS_EVIDENCE','unsupported_answer':False}
    if not sufficient or reference is None:
        return {'status':'incorrect','answerable':sufficient,'correctness':False,'numerical_error':None,
            'scientific_validity':'FAIL','unsupported_answer':True}
    error = compare(result['answer'],reference,task.answer_type)
    valid = error is not None and result.get('unit')==task.unit
    if result.get('approximate') and not task.approximation_allowed:
        valid = False
    correct = valid and error <= task.tolerance
    return {'status':'correct' if correct else 'incorrect','answerable':sufficient,'correctness':correct,
        'numerical_error':error,'scientific_validity':'PASS' if valid else 'FAIL','unsupported_answer':not valid}
