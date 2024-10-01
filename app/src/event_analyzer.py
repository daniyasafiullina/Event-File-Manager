class EventAnalyzer:
    @staticmethod
    def get_joiners_multiple_meetings_method(events):
        joiners_dict = {}
        for event in events:
            if event.joiners:
                for joiner in event.joiners:
                    if joiner.name in joiners_dict:
                        joiners_dict[joiner.name] += 1
                    else:
                        joiners_dict[joiner.name] = 1
        
        
        multiple_meeting_joiners = [joiner for joiner, count in joiners_dict.items() if count >= 2]
        
        return multiple_meeting_joiners
