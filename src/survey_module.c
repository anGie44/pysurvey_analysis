#include <stdio.h>
#include "Python.h"
#include "survey.h"

static PyObject *survey_sumarray(PyObject *self, PyObject *args) {
	PyObject *buf;
	if (!PyArg_ParseTuple(args, "O", &buf)) {
		return NULL;
	}

	Py_buffer view;
	int buf_flags = PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT;
	if (PyObject_GetBuffer(buf, &view, buf_flags) == -1) {
		return NULL;
	}

	if (strcmp(view.format, "d") != 0) {
		PyErr_SetString(PyExc_TypeError, "we only take floats :(");
		PyBuffer_Release(&view);
		return NULL;
	}

	double result = sumarray(view.buf, view.shape[0]);
	PyBuffer_Release(&view);
	return Py_BuildValue("d", result);
}

static PyMethodDef SurveyMethods[] = {
	{"sumarray", &survey_sumarray, METH_VARARGS, "Compute sum of an array"},
	{ NULL, NULL, 0, NULL}
};

static struct PyModuleDef survey_module = {
	.m_base = PyModuleDef_HEAD_INIT,
	.m_name = "survey_py",
	.m_size = -1, 
	.m_methods = SurveyMethods
};


PyMODINIT_FUNC PyInit_survey_(void) {
	return PyModule_Create(&survey_module);
}