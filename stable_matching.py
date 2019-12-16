import copy
import random

class StableMatching:
    def __init__(self,
                doctors, # set of doctor ids
                hospitals, # set of hospital ids
                doctor_preferences, # dict mapping doc_id => [h_id], where [h_id] is a preference-ordered list
                hospital_preferences, # dict mapping h_id => [doc_id], where [doc_id] is a preference-ordered list
                ):                    # doctor preferences must range over ENTIRE set of relevant alternatives  
        self.doctors = doctors
        self.hospitals = hospitals
        self.doctor_preferences = doctor_preferences
        self.hospital_preferences = hospital_preferences


    def compute_matching(self):
        free_doctors = copy.copy(self.doctors)
        doctor_matches = {}
        doctor_pref_idxs = {doc_id:0 for doc_id in free_doctors}
        hospital_matches = {}

        while len(free_doctors) > 0:
            # select free doctor 
            doc_id = random.sample(free_doctors, 1)[0]
            doc_idx = doctor_pref_idxs[doc_id]
            doctor_pref_idxs[doc_id] += 1

            # select index of the first un-proposed hospital
            doc_preferences = self.doctor_preferences[doc_id]
            assert(doc_idx < len(doc_preferences))
            proposal_h_id = doc_preferences[doc_idx]

            # try to match doctor to hospital
            if proposal_h_id not in hospital_matches:
                # if hospital is unmatched, enact the matching
                hospital_matches[proposal_h_id] = doc_id
                doctor_matches[doc_id] = proposal_h_id
                free_doctors.remove(doc_id)
            else:
                # if hospital is already matched, see if hospital prefers
                # this doctor over the incumbent
                incumbent_doc_id = hospital_matches[proposal_h_id]
                if self._compare_doctors(proposal_h_id, doc_id, incumbent_doc_id) == 1:
                    hospital_matches[proposal_h_id] = doc_id
                    doctor_matches[doc_id] = proposal_h_id
                    free_doctors.remove(doc_id)
                    free_doctors.add(incumbent_doc_id)

        return doctor_matches, hospital_matches
    
    def _compare_doctors(self, h_id, doc_id_1, doc_id_2):
        # returns 1 if h_id prefers doc_id_1, 0 if indifferent, -1 if prefers doc_id_2
        assert(h_id in self.hospitals)
        if h_id not in self.hospital_preferences:
            return 0

        h_prefs = self.hospital_preferences[h_id] 

        if doc_id_1 in h_prefs:
            pref_1 = h_prefs.index(doc_id_1)
        else:
            pref_1 = len(h_prefs)

        if doc_id_2 in h_prefs:
            pref_2 = h_prefs.index(doc_id_2)
        else:
            pref_2 = len(h_prefs)

        if pref_1 < pref_2:
            return 1
        elif pref_1 == pref_2:
            return 0
        else:
            return -1
