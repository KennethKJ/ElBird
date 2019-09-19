load imageList

%% Define paths
GoogleDrivePath = 'C:\Users\alert\Google Drive\';
photoPath = '\ML\Databases\Photo Booth User Group Photos\(2) Bird Photo Booth Users Group_files\';
Bird_dBpath = '\ML\Databases\Birds_dB\Images\';

%% Retrieve classes
f = dir([GoogleDrivePath Bird_dBpath]);
classes = {f(3:end).name}';



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

t(t.Label == '-' | t.Label == 'DELETE' ,:) = [];


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

C = {'',''};
for i = 1 : height(t)
    
    label = char(t.Label(i));
    
    label(strfind(label, ' ')) = '_';
    label(strfind(label, '-')) = '_';
    
%     idx = ismember(classes, lower(label));
%     disp(label)
%     [d, de]= strnearest(lower(label), classes);
%     
    
    
%     if sum(idx) == 1
%         disp(['Yes! : ' label])
%         
%     elseif sum(idx) == 0
%         
%         
        sex = t.Sex{i};
        
        if ~isempty(sex)
            label = [label '_' sex];
        end
        
        plumage = t.Plumage{i};
        if ~isempty(plumage)
           label = [label '_' plumage];
        end    
        
        
        disp('')
        if ~ismember(label,C(:,1))
            C{end+1,1} = label;
            
            [idx, distance]= strnearest(lower(label), classes);
            
            if distance < 1
                C{end,2} = classes(idx);
            end
            
        end
        
        
        
        
%         idx = ismember(classes, lower(label));
        
%         if sum(idx) == 0 % Not found in first round
            
%             plumage = t.Plumage{i};
%             if ~isempty(plumage)
%                 label = [label '_' plumage];
%             end
%             idx = ismember(classes, lower(label));
%             if sum(idx) == 0
%                 
%                 label = [label '_JUVENILE'];
%                 idx = ismember(classes, lower(label));
%                 if sum(idx) == 1
%                     disp(['Yes! : ' label])
%                     
%                 else
%                     disp(label)
%                     disp('Hopeless!')
%                 end
%             end
%         elseif sum(idx) == 1
%             disp(['Yes! : ' label])
%         else
%             disp('Fuck!')
%             
%         end
%         
%     else
%         disp('')
%         
%     end
%     disp('')
    
end


disp('')


