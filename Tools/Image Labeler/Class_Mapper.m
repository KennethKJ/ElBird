function Class_Mapper()

load imageList

%% Define paths
GoogleDrivePath = 'C:\Users\alert\Google Drive\';
photoPath = '\ML\Databases\Photo Booth User Group Photos\(2) Bird Photo Booth Users Group_files\';
Bird_dBpath = '\ML\Databases\Birds_dB\Images\';

%% Retrieve classes
f = dir([GoogleDrivePath Bird_dBpath]);
classes = {f(3:end).name}';


classes{end+1} = 'IGNORE';

t = struct2table(list);

t.folder = [];
t.date = [];
t.isdir = [];
t.datenum = [];
t.bytes = [];

C = t.Label;

for i = 1 : length(C)
    
    if isempty(C{i})
        C{i} = '-';
    end
    
    
end

t.Label = C;
t.Label = categorical(t.Label);

t(t.Label == '-' | t.Label == 'DELETE' | t.Label == 'TWO OR MORE' | t.Label == 'UNKNOWN'| t.Label == 'NON-BIRD',:) = [];


%% Remove pics with more than one bird (for now)
t.name = categorical(t.name);

moreThanOneIdx = zeros(height(t),1);

for i = 1 : height(t)
    idx = t.name == t.name(i);
    if sum(idx) > 1
        moreThanOneIdx = moreThanOneIdx + idx;
    end
end
moreThanOneIdx = moreThanOneIdx > 0;

t(moreThanOneIdx,:) = [];

disp('')

%% Get all existing labels
C = {};
for i = 1 : height(t)
    
   label = char(t.Label(i));
   
   if ~isempty(t.Sex{i})
       label = [label '_' t.Sex{i}];
   end
   
   if ~isempty(t.Plumage{i})
       label = [label '_' t.Plumage{i}];
   end
   
   if ~ismember(label, C)
       C{end+1} = label;
   end
   
   t.totalLabel(i) = {label};
   
end

t.totalLabel = categorical(t.totalLabel);

C = C';

totalLabels = unique(t.totalLabel);

load map113-Sep-2019.mat

for i = 1 : length(totalLabels)
    
    
    t2 = t(t.totalLabel == totalLabels(i),:); 
    
    l = char(totalLabels(i));
    idx = ismember(C2(:,1),l);
    
    folder = classes{ismember(classes, C2{idx,2})};
    
    for j = 1 : height(t2)
        
        if copyfile([GoogleDrivePath photoPath char(t2.name(j))],[GoogleDrivePath Bird_dBpath folder '\pb_Ex_' num2str(j) '.jpg'])
        
        else
            disp(l)
        end
            
    end
    
    
    
end

% 
% figure(1); clf;
% h = 0.026;
% dividor = ceil(length(C)/2);
% L = 0;
% fact = 0;
% classes{end+1} = 'IGNORE';
% H = zeros(length(C),1); 
% 
% for i = 1 : length(C)
%     
%    if i == dividor
%        L = L + 0.5;
%        fact= dividor;
%    end
%     
%    
%    
%     uicontrol(1, ...
%         'Units','Normalized',  ...
%         'Position',[L, 0.98-(i-fact)*h, 0.2, h], ...
%         'String',C(i), ...
%         'FontSize',8)
%     
%     H(i) = uicontrol(1, ...
%         'Units','Normalized',  ...
%         'Position',[L+0.2, 0.98-(i-fact)*h, 0.2, h], ...
%         'String',classes, ...
%         'FontSize',8, ...
%         'Style','Popupmenu');
%     
%     
% end
% 
% 
%     uicontrol(1, ...
%         'Units','Normalized',  ...
%         'Position',[0 0.01 0.3, 0.04], ...
%         'String','Save', ...
%         'FontSize',8, ...
%         'Style','pushbutton',...
%         'Callback', {@saveMap,H, C});
%     
%     uicontrol(1, ...
%         'Units','Normalized',  ...
%         'Position',[0 0.01 0.3, 0.04], ...
%         'String','Save', ...
%         'FontSize',8, ...
%         'Style','pushbutton',...
%         'Callback', {@copyAndMoveFiles, t, classes});
% 
% function saveMap(a, b, H, C)
% 
% global C2
% 
% disp('')
% C2 = cell(length(H),2);
% for i = 1 : length(H)
%     
%     s = get(H(i), 'String');
%     value = get(H(i), 'Value');
%     
%     C2{i,1} = C{i};
%     C2{i,2} = s(value);
%     
% end
% save(['map' date '.mat'],'C2')
% 
% function copyAndMoveFiles(a, b, t, C)
% 
% global C2 GoogleDrivePath photoPath Bird_dBpath 
% 
% 
% 
% 
% for i = 1 : height(t)
%     
%     
%     
%     
% end
% 
% 
% disp('')
% 





