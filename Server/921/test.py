import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import numpy as np
import cv2
import matplotlib.pyplot as plt
import segmentation_models_pytorch as smp

import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset as BaseDataset
import albumentations as albu
from tensorboardX import SummaryWriter
from attention_unet import AttU_Net
from attention_unet2 import resnet34_unet as ResNet_attUnet

DATA_DIR = '/home/system/datasets/gallbladder1/crop'
x_train_dir = os.path.join(DATA_DIR, 'train/img')
y_train_dir = os.path.join(DATA_DIR, 'train/mask')

x_valid_dir = os.path.join(DATA_DIR, 'val/img')
y_valid_dir = os.path.join(DATA_DIR, 'val/mask')

x_test_dir = os.path.join(DATA_DIR, 'test/img')
y_test_dir = os.path.join(DATA_DIR, 'test/mask')
# helper function for data visualization
def visualize(**images):
    """PLot images in one row."""
    n = len(images)
    plt.figure(figsize=(16, 5))
    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image)
    plt.show()


class Dataset(BaseDataset):
    """CamVid Dataset. Read images, apply augmentation and preprocessing transformations.

    Args:
        images_dir (str): path to images folder
        masks_dir (str): path to segmentation masks folder
        class_values (list): values of classes to extract from segmentation mask
        augmentation (albumentations.Compose): data transfromation pipeline
            (e.g. flip, scale, etc.)
        preprocessing (albumentations.Compose): data preprocessing
            (e.g. noralization, shape manipulation, etc.)

    """

    CLASSES = ['0', 'gallbladder']

    def __init__(
            self,
            images_dir,
            masks_dir,
            classes=None,
            augmentation=None,
            preprocessing=None,
    ):
        self.ids = os.listdir(images_dir)
        self.images_fps = [os.path.join(images_dir, image_id) for image_id in self.ids]
        self.masks_fps = [os.path.join(masks_dir, image_id).split('.')[0] + '_gt.png' for image_id in self.ids]

        # convert str names to class values on masks
        self.class_values = [self.CLASSES.index(cls.lower()) for cls in classes]

        self.augmentation = augmentation
        self.preprocessing = preprocessing

    def __getitem__(self, i):

        # read data
        image = cv2.imread(self.images_fps[i])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(self.masks_fps[i], -1)  # png16   -1
        #         print(self.class_values)
        # extract certain classes from mask (e.g. cars)
        masks = [(mask == v) for v in self.class_values]
        mask = np.stack(masks, axis=-1).astype('float')
        #         mask[mask != 0] = 1
        #         print(mask.max())
        # apply augmentations
        if self.augmentation:
            sample = self.augmentation(image=image, mask=mask)
            image, mask = sample['image'], sample['mask']

        # apply preprocessing
        if self.preprocessing:
            sample = self.preprocessing(image=image, mask=mask)
            image, mask = sample['image'], sample['mask']

        return image, mask

    def __len__(self):
        return len(self.ids)


def get_training_augmentation():
    train_transform = [

        albu.HorizontalFlip(p=0.5),

        albu.ShiftScaleRotate(scale_limit=0.5, rotate_limit=0, shift_limit=0.1, p=1, border_mode=0),

        #         albu.PadIfNeeded(min_height=320, min_width=320, always_apply=True, border_mode=0),
        #         albu.RandomCrop(height=320, width=320, always_apply=True),

        #         albu.IAAAdditiveGaussianNoise(p=0.2),
        #         albu.IAAPerspective(p=0.5),

        #         albu.OneOf(
        #             [
        #                 albu.CLAHE(p=1),
        # #                 albu.RandomBrightness(p=1),
        # #                 albu.RandomGamma(p=1),
        #             ],
        #             p=0.9,
        #         ),

        #         albu.OneOf(
        #             [
        #                 albu.IAASharpen(p=1),
        #                 albu.Blur(blur_limit=3, p=1),
        #                 albu.MotionBlur(blur_limit=3, p=1),
        #             ],
        #             p=0.9,
        #         ),

        #         albu.OneOf(
        #             [
        #                 albu.RandomContrast(p=1),
        #                 albu.HueSaturationValue(p=1),
        #             ],
        #             p=0.9,
        #         ),
    ]
    return albu.Compose(train_transform)


def get_validation_augmentation():
    """Add paddings to make image shape divisible by 32"""
    test_transform = [
        #         albu.PadIfNeeded(384, 480)
    ]
    return albu.Compose(test_transform)


def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')


def get_preprocessing(preprocessing_fn):
    """Construct preprocessing transform

    Args:
        preprocessing_fn (callbale): data normalization function
            (can be specific for each pretrained neural network)
    Return:
        transform: albumentations.Compose

    """

    _transform = [
        albu.Lambda(image=preprocessing_fn),
        albu.Lambda(image=to_tensor, mask=to_tensor),
    ]
    return albu.Compose(_transform)

ENCODER = 'se_resnext50_32x4d'
ENCODER_WEIGHTS = 'imagenet'
CLASSES = ['gallbladder']
ACTIVATION = 'sigmoid' # could be None for logits or 'softmax2d' for multicalss segmentation
DEVICE = 'cuda'
write = SummaryWriter('logs')
# create segmentation model with pretrained encoder
# model = smp.Unet(
# #     encoder_name=ENCODER,
#     encoder_weights=ENCODER_WEIGHTS,
#     classes=len(CLASSES),
#     activation=ACTIVATION,
# )
model = ResNet_attUnet(3,1)
# model = torch.load("models/resattunet_best_model_0.71.pth")
# model_dict = torch.load("models/resattunet_best_model_3att.pth").state_dict()
# 载入参数
# model.load_state_dict(model_dict)
# model = AttU_Net(3,1)
preprocessing_fn = smp.encoders.get_preprocessing_fn(ENCODER, ENCODER_WEIGHTS)

train_dataset = Dataset(
    x_train_dir,
    y_train_dir,
#     augmentation=get_training_augmentation(),
    preprocessing=get_preprocessing(preprocessing_fn),
    classes=CLASSES,
)

valid_dataset = Dataset(
    x_valid_dir,
    y_valid_dir,
#     augmentation=get_validation_augmentation(),
    preprocessing=get_preprocessing(preprocessing_fn),
    classes=CLASSES,
)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=0)
valid_loader = DataLoader(valid_dataset, batch_size=8, shuffle=False, num_workers=0)

i = 0
for img, msk in train_loader:
    if i == 0:
        img = np.array(img)
        msk = np.array(msk)
        print(img.max())
        print(msk.max())
        visualize(
            image=img[0].transpose(1, 2, 0),
            gallbladder_mask=msk[0].transpose(1, 2, 0).squeeze(),
        )
    else:
        break
    i+=1

# Dice/F1 score - https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
# IoU/Jaccard score - https://en.wikipedia.org/wiki/Jaccard_index
EPOCHS = 50
loss = smp.utils.losses.DiceLoss()
metrics = [
    smp.utils.metrics.IoU(threshold=0.5),
    smp.utils.metrics.Fscore(),
    smp.utils.metrics.Accuracy(),
    smp.utils.metrics.Recall(),
    smp.utils.metrics.Precision(),
]
# optimizer = torch.optim.SGD([
#     dict(params=model.parameters(), lr=0.001, momentum=0.8),
# ])
optimizer = torch.optim.Adam([
    dict(params=model.parameters(), lr=0.01),
])
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, EPOCHS, eta_min=1e-5)
# scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[5, 8, 10, 15, 20], gamma=0.1)

# create epoch runners
# it is a simple loop of iterating over dataloader`s samples
train_epoch = smp.utils.train.TrainEpoch(
    model,
    loss=loss,
    metrics=metrics,
    optimizer=optimizer,
    device=DEVICE,
    verbose=True,
)

valid_epoch = smp.utils.train.ValidEpoch(
    model,
    loss=loss,
    metrics=metrics,
    device=DEVICE,
    verbose=True,
)

# train model for 40 epochs

max_score = 0

for i in range(0, EPOCHS):
    lr = scheduler.get_last_lr()
    print('\nEpoch: {},lr:{}'.format(i, lr))
    train_logs = train_epoch.run(train_loader)
    valid_logs = valid_epoch.run(valid_loader)

    # do something (save model, change lr, etc.)
    if max_score < valid_logs['iou_score']:
        max_score = valid_logs['iou_score']
        torch.save(model, './models/attunet_best_model.pth')
        print('Model saved!')
    scheduler.step(i)
    write.add_scalars('Train_val_loss', {'train_loss' + str(EPOCHS): train_logs['dice_loss']}, i + 1)
    write.add_scalars('Train_val_loss', {'val_loss' + str(EPOCHS): valid_logs['dice_loss']}, i + 1)
    write.add_scalars('IoU_score', {'train_IoU_score' + str(EPOCHS): train_logs['iou_score']}, i + 1)
    write.add_scalars('IoU_score', {'val_IoU_score' + str(EPOCHS): valid_logs['iou_score']}, i + 1)
    write.add_scalars('f_score', {'train_fscore' + str(EPOCHS): train_logs['fscore']}, i + 1)
    write.add_scalars('f_score', {'val_fscore' + str(EPOCHS): valid_logs['fscore']}, i + 1)
    write.add_scalars('accuracy', {'train_accuracy' + str(EPOCHS): train_logs['accuracy']}, i + 1)
    write.add_scalars('accuracy', {'val_accuracy' + str(EPOCHS): valid_logs['accuracy']}, i + 1)
    write.add_scalars('recall', {'train_recall' + str(EPOCHS): train_logs['recall']}, i + 1)
    write.add_scalars('recall', {'val_recall' + str(EPOCHS): valid_logs['recall']}, i + 1)
    write.add_scalars('precision', {'train_precision' + str(EPOCHS): train_logs['precision']}, i + 1)
    write.add_scalars('precision', {'val_precision' + str(EPOCHS): valid_logs['precision']}, i + 1)
    if i < 2:
        #         optimizer.param_groups[0]['lr'] = 1e-5
        #         print('Decrease decoder learning rate to 1e-5!')
        print('valid_logs', valid_logs)
        print('train_logs', train_logs)