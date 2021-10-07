> ## 2021 Software Contest

- 2021 소프트웨어 경진대회
- 주제: YOLO를 이용한 자동 분류 시스템
- Recyclear (AIC)
- 작성에 기여한 부분이 있는 코드 모음
- 2021.05.13 ~ 2021.08.19

---

### darknet에 이용된 학습 코드

[Darknet - YOLO4](https://github.com/AlexeyAB/darknet)

<!-- ./darknet detector calc_anchors custom/custom_path.data custom/custom_parameter.cfg -num_of_clusters 9 -width 608 -height 608 -->

- ./darknet detector train custom/custom_path.data custom/custom_parameter.cfg yolov4.conv.137 -map
- ./darknet detector map custom/cusotm_path.data custom/custom_parameter.cfg backup/custom_parameter_best.weights

<br />

- ./darknet detect custom/custom_parameter.cfg backup/custom_parameter_best.weights custom/test.jpg
- ./darknet detector test custom/custom_path.data custom/custom_parameter.cfg backup/custom_parameter_best.weights -dont_show -ext_output < test.txt > test_results.txt
