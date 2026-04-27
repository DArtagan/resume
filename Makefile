.PHONY: view, resume

#examples: $(foreach x,coverletter cv resume,examples/$x.pdf)

view: resume
	open resume.pdf

resume: 
	xelatex resume.tex

#%.pdf: %.tex
#	xelatex -output-directory=$(dir $@) $<
