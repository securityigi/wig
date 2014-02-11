from plugins.classes.requester import Requester
from plugins.classes.specializedMatchers import MD5Matcher, StringMatcher, RegexMatcher, HeaderMatcher


class CMSReq(Requester):
	def __init__(self, host, cache, results):
		super().__init__(host, cache, results)
		self.category = "CMS"
		self.match_class = None

	def prepare_results(self, matches):
		data = []
		for m in matches:
			url = m['response'].url
			version = m['output']
			weight = m['weight'] if 'weight' in m else 1
			
			for d in data:
				if d['url'] == url:
					d['count'] += weight
					break
			else:
				data.append( {'url': url, 'count': weight, 'version': version} )

		return data

	def run(self):
		# make requests
		requested = self.request_uniq()

		# find matches
		matcher = self.match_class(requested)
		matches = matcher.get_matches()

		# add to results
		intermediate_results = self.prepare_results(matches)
		self.add_results(intermediate_results)



class CMSReqMD5(CMSReq):
	def __init__(self, host, cache, results):
		super().__init__(host, cache, results)
		self.match_class = MD5Matcher
		self.use_weights = True


class CMSReqString(CMSReq):
	def __init__(self, host, cache, results):
		super().__init__(host, cache, results)
		self.match_class = StringMatcher


class CMSReqRegex(CMSReq):
	def __init__(self, host, cache, results):
		super().__init__(host, cache, results)
		self.match_class = RegexMatcher

class CMSReqHeader(CMSReq):
	def __init__(self, host, cache, results):
		super().__init__(host, cache, results)
		self.match_class = HeaderMatcher



