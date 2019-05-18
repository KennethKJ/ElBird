
clear all
clc

dB_path = 'C:/Users/Kenneth Kragh Jensen/Google Drive/ML/Databases/Unified Feeder Birds Database/Images/';

newLocation =  'C:/Users/Kenneth Kragh Jensen/Google Drive/ML/Databases/Birds_dB/Images/';


mkdir(newLocation)

errors = 0;

cd(dB_path);
folders= dir('*.*');
folders(1:2) = []; % remove the dots

for i = 1 : length(folders)
    
    % Get current folder
    origFolder = folders(i).name;
    % Remove any spaces in fodler names
    currentFolder = rmChars(origFolder);
    currentFolder = rmDoubleChars(currentFolder);
    currentFolder = lower(currentFolder);
    
    % MAke new directory in new database with out the spaces
    mkdir([newLocation currentFolder])
    
    
    % Go to old database folder
    cd([dB_path folders(i).name]);
    % Get files there as struct
    files = dir('*.jpg');
    for f = 1 : length(files)
        origFile = files(f).name;
        currentFile  = ['Ex' num2str(f) '.jpg'];
        
        orig = [dB_path origFolder '/' origFile];
        dest = [newLocation currentFolder '/' currentFile];
        
        try
            copyfile(orig, dest)
        catch ERROR
            errors = errors + 1;
           disp(ERROR.message) 
        end

        disp(dest)
        
    end

    
    
    
end





disp('Done')
disp(['Total erroes = ' num2str(errors)])

function string = rmChars(string)


illegalChars = ' -,.:;!\|/?()[]*?#"''';
replaceChar = '_';

for c = 1 : length(illegalChars)
    
    k = strfind(string, illegalChars(c));
    if k == length(string)
        % Just remove altogther if at end of string
        string(k) = [];

    else
        string(k) = replaceChar;
    end
end

end

function string = rmDoubleChars(string)

illegalChars = '__';

for c = 1 : length(illegalChars)
    
    k = strfind(string, illegalChars);
    if ~isempty(k)
        % Just remove altogther if at end of string
        string(k) = [];

    end
end

end




