#include<Python.h>
#include<ndarrayobject.h>
#include<algorithm>





typedef struct {
    PyObject_HEAD
    int munmap_size;
    void *memory;
} _MyDeallocObject;

static void
_mydealloc_dealloc(PyObject *obj)
{

    _MyDeallocObject * obj_= (_MyDeallocObject*)obj;
   // munlock(obj_->memory,obj_->munmap_size);
    munmap(obj_->memory,obj_->munmap_size);
    Py_TYPE(obj_)->tp_free((PyObject *)obj_);

}

PyTypeObject _MyDeallocType = {
        PyVarObject_HEAD_INIT(NULL, 0)          /*var head*/
        "module.instance",                              /*tp_name*/
        sizeof(_MyDeallocObject),                       /*tp_basicsize*/
        0,                                              /*tp_itemsize*/
        _mydealloc_dealloc                             /*tp_dealloc*/
        };



static PyObject * readFields_column_min_zero_copy(PyObject * self,PyObject * args)
{
    import_array();
    char * filename;
    char * field_name;
    long start_tick;
    long end_tick;

    if(!PyArg_ParseTuple(args,"slls",&filename,&start_tick,&end_tick,&field_name))
        return NULL;
    int size;
    int noise_shift;
    void * data= read_data_min_raw(filename,start_tick,end_tick,field_name,size,noise_shift);
    PyObject * newobj, * arr=NULL;

    npy_intp  DIM[1]{size};
    arr=PyArray_SimpleNewFromData(1,DIM,NPY_INT,data+noise_shift);


    newobj =(PyObject*) PyObject_New(_MyDeallocObject, &_MyDeallocType);

    ((_MyDeallocObject *)newobj)->memory =data;
    ((_MyDeallocObject *)newobj)->munmap_size=UPPER_ALIGN_TO_PAGE(size*sizeof(int))+noise_shift;
    PyArray_BASE((PyArrayObject *)arr) = newobj;

    return arr;
}




static PyMethodDef JsmmapMethods[] = {
        {"readFields_column_min_zero_copy",readFields_column_min_zero_copy,METH_VARARGS,"readFields_column_min_zero_copy"},
        {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef Jsmmapmodule = {
        PyModuleDef_HEAD_INIT,
        "ttreader",   /* name of module */
        NULL, /* module documentation, may be NULL */
        -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
        JsmmapMethods
};


PyMODINIT_FUNC PyInit_Ttreader(void) {
    PyObject *m;

    m = PyModule_Create(&Jsmmapmodule);
    if (m == NULL)
        return NULL;

    _MyDeallocType.tp_new=PyType_GenericNew;
    _MyDeallocType.tp_flags = Py_TPFLAGS_DEFAULT;
    _MyDeallocType.tp_doc = "object help to munmap";
    _MyDeallocType.tp_free=[](void *){};

    if (PyType_Ready(&_MyDeallocType) < 0)
        return NULL;
    Py_INCREF(&_MyDeallocType);
    PyModule_AddObject(m, "MyDealloc", (PyObject *) &_MyDeallocType);


    ArrayTypeError = PyErr_NewException("arrayType.error", NULL, NULL);
    Py_INCREF(ArrayTypeError);
    PyModule_AddObject(m, "error", ArrayTypeError);

    return m;
}