from sigpy import get_faculty, get_school_year

target = "201403027"
stalker = "201403027"
p = ""

fac = get_faculty("feup")
fac.login(stalker, p)
target = fac.get_student(target)

for c in target.courses:  # iterate the target courses
	if c.id:  # if it has a valid id
		target_classes = []

		# load the course
		course = fac.get_course((c.id, get_school_year()))
		print(course.name)

		# load the study plan, so we can get the subjects taught in course
		study_plan = fac.get_study_plan((course.study_plan.id, course.study_plan.year))
		# merge valid mandatory and optional courses and get their ids
		subjects = [s.id for y in study_plan.years for sm in y.semesters for s in sm.subjects if s.code != ""] + [s.id for s in study_plan.optionals if s.code != ""]

		# remove None values and duplicates
		subjects = list(set(filter(lambda x: x, subjects)))

		# load all the subjects (if this is not in cache will take some time)
		# use the following to provide feedback of the progress instead of the silent one
		# subjects = [[fac.get_subject(s), print(s.name)][0] for s in subjects]
		subjects = [fac.get_subject(s) for s in subjects]

		# now that we have every subject for this course, we will iterate them
		for s in subjects:
			print(s.name)
			# load the classes (one subject has many classes, like 1MIEIC01, ...)
			classes = fac.get_classes((course.id, s.id, get_school_year(), s.semester))
			for i, cl in enumerate(classes.classes):  # iterate these classes to look for our target
				for st in cl.students:  # iterate each student of each class
					if st.name == target.name:  # if it is our target, we hve another piece of the puzzle!!
						target_classes.append("%s.%s" % (s.initials, classes.class_names[i].name))  # save it

		print(target_classes)

		# semester = subjects[0].semester  # assume it is the same semester for all
		semester = 1  # or hardcode because it sometimes fails

		# get the TTS link, if there is a class with a wrong name
		# that is a problem on TTS' side!
		print("https://ni.fe.up.pt/TTS/#%s!%s!%s-%s~%s" % (get_school_year(), semester, fac.name.upper(), course.initials, "~".join(target_classes)))
