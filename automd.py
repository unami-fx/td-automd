"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import os

class automd:
	"""
	md maker for td
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Operator(self, effect):
		markdown = f"## {effect.name}\n\n"
		markdown += f"{effect.comment}\n\n"
		markdown += f"### Parameters\n\n"
		pages = effect.customPages
		for page in pages:
			markdown += f"### {page.name}\n\n"
			parameters = page.parGroups
			for _par in parameters:
				style = _par.style.lower()
				if style == "header": 
					continue
				n = len(_par)
				markdown += f"<b>{_par.label}</b> `{style}{n if n>1 else ''}` - {_par.help or 'No definition provided'}<br>\n"
			markdown += "\n"
		return markdown
			
	def CreateMD(self, operator, folder, filename):
		automd = self.Operator(operator)
		mdfile =  f"{folder}/{filename or operator.name}.md"
		os.makedirs(os.path.dirname(mdfile), exist_ok=True)
		with open(mdfile, "w", encoding="utf-8") as f:
			f.write(automd)