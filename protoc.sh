export PROTO_PATH=$(pwd)/proto
export PACKAGE_PATH=$(pwd)/source/identity/api/proto/

mkdir -p $PACKAGE_PATH

for i in $(find $PROTO_PATH -name '*.proto');
do
    python -m grpc_tools.protoc -I $PROTO_PATH --python_out=$PROTO_PATH --grpc_python_out=$PROTO_PATH $i
done;

for i in $(find $PROTO_PATH -name '*_pb2*.py');
do
  mv $i $PACKAGE_PATH
done;