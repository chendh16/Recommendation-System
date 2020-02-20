source path_config.sh

echo "sample test..."
alpha_array=("0.0")
for alpha in ${alpha_array[@]}
do
  echo "sample on "alpha
  path_rnn_sample_out_file_path="./data/output/path_rnn_test_samples_"$alpha".txt"
  fmg_sample_out_file_path="./data/output/fmg_data/fmg_test_samples_"$alpha".txt"
  python3 sample.py $alpha $user_id_file_path $movie_fq_path $test_pos_tuple_path $test_neg_tuple_path \
                    $path_rnn_sample_out_file_path $fmg_sample_out_file_path
done
