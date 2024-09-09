import grpc
from containerd.services.namespaces.v1 import namespace_pb2, namespace_pb2_grpc

with grpc.insecure_channel("unix:///run/containerd/containerd.sock") as channel:
	namespacev1 = namespace_pb2_grpc.NamespacesStub(channel)
	namespaces = namespacev1.List(namespace_pb2.ListNamespacesRequest()).namespaces
	for namespace in namespaces:
		print("namespace:", namespace.name)
