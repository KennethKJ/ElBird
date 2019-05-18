function varargout = ImageLabeler(varargin)
% IMAGELABELER MATLAB code for ImageLabeler.fig
%      IMAGELABELER, by itself, creates a new IMAGELABELER or raises the existing
%      singleton*.
%
%      H = IMAGELABELER returns the handle to a new IMAGELABELER or the handle to
%      the existing singleton*.
%
%      IMAGELABELER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in IMAGELABELER.M with the given input arguments.
%
%      IMAGELABELER('Property','Value',...) creates a new IMAGELABELER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ImageLabeler_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to ImageLabeler_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ImageLabeler

% Last Modified by GUIDE v2.5 14-Dec-2018 20:23:58

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @ImageLabeler_OpeningFcn, ...
                   'gui_OutputFcn',  @ImageLabeler_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before ImageLabeler is made visible.
function ImageLabeler_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to ImageLabeler (see VARARGIN)

% Choose default command line output for ImageLabeler
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes ImageLabeler wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = ImageLabeler_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)




