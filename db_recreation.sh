#! /bin/bash
set -eu 

echo -n "What is your operation system? [W if Window, L if Linux]: "
read var

if [[ $var == 'L' ]]
then
    call_python='python'
elif [[ $var == 'W' ]]
then
    call_python='py'
fi

$call_python -m main_files.table_deletion
$call_python -m main_files.table_creation
$call_python -m main_files.table_insertion_branch
$call_python -m main_files.table_insertion_payment
$call_python -m main_files.table_insertion_product
$call_python -m main_files.table_insertion_orders