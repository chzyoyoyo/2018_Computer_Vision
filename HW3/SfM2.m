function SfM2(one,two,visualize)
if nargin==3
    visualize=true;
else
    visualize=false;
end
[path,~,~]=fileparts(one);
[~,filename,~]=fileparts(path);
res_dir='result/';
untitle=0;
if strcmp(filename,'')
    while true
        filename=[res_dir,'untitled',untitle];
        if exist(filename,'file')
            untitle=untitle+1;
        else
            break;
        end
    end
end

img0 = imread(one);
img1 = imread(two);
intrinsic1=(dlmread(fullfile(path,'intrinsic.new')))';
intrinsic2=(dlmread(fullfile(path,'intrinsic2.new')))';

%% match features
[mp1, mp2]=matchFeaturePoints(img0,img1,0.01);
% figure
showMatchedFeatures(img0, img1, mp1, mp2);

%% Estimate F R t
[F, inliersIdx] = RANSAC(mp1, mp2);
% Find epipolar inliers
inlierPoints1 = mp1(inliersIdx, :);
inlierPoints2 = mp2(inliersIdx, :);
% figure
showMatchedFeatures(img0, img1, inlierPoints1, inlierPoints2);
[R, t] = motionFromF(F, intrinsic1, intrinsic2, inlierPoints1, inlierPoints2);
camMat0 = [eye(3); [0 0 0]]*intrinsic1;
camMat1 = [R; -t*R]*intrinsic2;

%% dense match
[mp1, mp2]=matchFeaturePoints(img0,img1,0.0001);
points3D = mytriangulation(mp1, mp2, camMat0, camMat1);

%% output textured object file
obj_main(points3D, double(mp1), camMat0', one, filename);

%% plot
cls = reshape(img0, [size(img0, 1) * size(img0, 2), 3]);
colorIdx = sub2ind([size(img0, 1), size(img0, 2)], round(mp1(:,2)),round(mp1(:, 1)));
ptCloud = pointCloud(points3D, 'Color', cls(colorIdx, :));
if visualize
    figure
    pcshow(ptCloud, 'VerticalAxis', 'y', 'VerticalAxisDir', 'down', 'MarkerSize', 45);
end
