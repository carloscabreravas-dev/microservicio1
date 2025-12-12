#!/usr/bin/env python3
"""
Script auxiliar para gestionar despliegues en OpenShift
Proporciona funciones útiles para monitoreo y troubleshooting
"""

import os
import sys
import subprocess
import json
import argparse
from typing import Optional, List, Dict
from datetime import datetime

class OpenShiftManager:
    """Gestor de despliegues en OpenShift"""
    
    def __init__(self):
        self.server = os.getenv("OPENSHIFT_SERVER")
        self.token = os.getenv("OPENSHIFT_TOKEN")
        self.namespace = os.getenv("OPENSHIFT_NAMESPACE", "default")
        
        if not all([self.server, self.token, self.namespace]):
            print("❌ Error: Variables de entorno no configuradas")
            print("   OPENSHIFT_SERVER, OPENSHIFT_TOKEN, OPENSHIFT_NAMESPACE")
            sys.exit(1)
    
    def run_command(self, cmd: List[str], capture_output: bool = False) -> Optional[str]:
        """Ejecutar comando oc"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                check=True
            )
            return result.stdout.strip() if capture_output else None
        except subprocess.CalledProcessError as e:
            print(f"❌ Error ejecutando comando: {' '.join(cmd)}")
            print(f"   {e.stderr}")
            return None
    
    def login(self) -> bool:
        """Autenticarse en OpenShift"""
        print("🔐 Autenticando...")
        cmd = [
            "oc", "login",
            f"--server={self.server}",
            f"--token={self.token}",
            "--insecure-skip-tls-verify=true"
        ]
        result = self.run_command(cmd)
        if result is None:
            print("✓ Autenticación completada")
            return True
        return False
    
    def get_status(self) -> Dict:
        """Obtener estado general del despliegue"""
        print("\n📊 Estado del despliegue:")
        print("=" * 50)
        
        status = {
            "deployment": self.get_deployment_status(),
            "pods": self.get_pods_status(),
            "services": self.get_services(),
            "routes": self.get_routes(),
            "hpa": self.get_hpa_status()
        }
        
        return status
    
    def get_deployment_status(self) -> Dict:
        """Obtener estado del deployment"""
        cmd = [
            "oc", "get", "deployment/microservicio",
            f"-n{self.namespace}",
            "-o", "json"
        ]
        output = self.run_command(cmd, capture_output=True)
        if output:
            data = json.loads(output)
            spec = data.get("spec", {})
            status = data.get("status", {})
            print(f"\n🚀 Deployment: microservicio")
            print(f"   Réplicas deseadas: {spec.get('replicas', 0)}")
            print(f"   Réplicas listas: {status.get('readyReplicas', 0)}")
            print(f"   Réplicas actualizadas: {status.get('updatedReplicas', 0)}")
            return status
        return {}
    
    def get_pods_status(self) -> List[Dict]:
        """Obtener estado de los pods"""
        cmd = [
            "oc", "get", "pods",
            f"-n{self.namespace}",
            "-l", "app=microservicio",
            "-o", "json"
        ]
        output = self.run_command(cmd, capture_output=True)
        if output:
            data = json.loads(output)
            pods = []
            print(f"\n📦 Pods:")
            for item in data.get("items", []):
                pod_name = item.get("metadata", {}).get("name")
                phase = item.get("status", {}).get("phase")
                containers = item.get("spec", {}).get("containers", [])
                print(f"   {pod_name}: {phase}")
                pods.append({"name": pod_name, "phase": phase})
            return pods
        return []
    
    def get_services(self) -> List[Dict]:
        """Obtener servicios"""
        cmd = [
            "oc", "get", "svc",
            f"-n{self.namespace}",
            "-l", "app=microservicio",
            "-o", "json"
        ]
        output = self.run_command(cmd, capture_output=True)
        if output:
            data = json.loads(output)
            services = []
            print(f"\n🔗 Servicios:")
            for item in data.get("items", []):
                svc_name = item.get("metadata", {}).get("name")
                svc_type = item.get("spec", {}).get("type")
                print(f"   {svc_name} ({svc_type})")
                services.append({"name": svc_name, "type": svc_type})
            return services
        return []
    
    def get_routes(self) -> List[Dict]:
        """Obtener rutas"""
        cmd = [
            "oc", "get", "routes",
            f"-n{self.namespace}",
            "-o", "json"
        ]
        output = self.run_command(cmd, capture_output=True)
        if output:
            data = json.loads(output)
            routes = []
            print(f"\n🌐 Rutas:")
            for item in data.get("items", []):
                route_name = item.get("metadata", {}).get("name")
                host = item.get("spec", {}).get("host")
                print(f"   {route_name}: https://{host}")
                routes.append({"name": route_name, "host": host})
            return routes
        return []
    
    def get_hpa_status(self) -> Dict:
        """Obtener estado del HPA"""
        cmd = [
            "oc", "get", "hpa",
            f"-n{self.namespace}",
            "-o", "json"
        ]
        output = self.run_command(cmd, capture_output=True)
        if output:
            data = json.loads(output)
            if data.get("items"):
                item = data["items"][0]
                spec = item.get("spec", {})
                status = item.get("status", {})
                print(f"\n📈 Auto-Escalado (HPA):")
                print(f"   Mín. réplicas: {spec.get('minReplicas', 0)}")
                print(f"   Máx. réplicas: {spec.get('maxReplicas', 0)}")
                print(f"   Réplicas actuales: {status.get('currentReplicas', 0)}")
                print(f"   CPU actual: {status.get('currentCPUUtilizationPercentage', 'N/A')}%")
                return status
        return {}
    
    def view_logs(self, follow: bool = False, tail: int = 50):
        """Ver logs de la aplicación"""
        print(f"\n📋 Logs (últimas {tail} líneas):")
        print("=" * 50)
        
        cmd = [
            "oc", "logs",
            f"-n{self.namespace}",
            "-l", "app=microservicio",
            f"--tail={tail}"
        ]
        
        if follow:
            cmd.insert(2, "-f")
        
        self.run_command(cmd)
    
    def describe_pod(self, pod_name: Optional[str] = None):
        """Describir un pod"""
        if not pod_name:
            # Obtener el primer pod
            cmd = [
                "oc", "get", "pods",
                f"-n{self.namespace}",
                "-l", "app=microservicio",
                "-o", "jsonpath={.items[0].metadata.name}"
            ]
            pod_name = self.run_command(cmd, capture_output=True)
        
        if pod_name:
            print(f"\n📝 Describiendo pod: {pod_name}")
            print("=" * 50)
            cmd = ["oc", "describe", "pod", pod_name, f"-n{self.namespace}"]
            self.run_command(cmd)
    
    def restart_deployment(self):
        """Reiniciar el deployment"""
        print(f"\n🔄 Reiniciando deployment...")
        cmd = [
            "oc", "rollout", "restart",
            f"-n{self.namespace}",
            "deployment/microservicio"
        ]
        if self.run_command(cmd) is not None:
            print("✓ Deployment reiniciado")
            
            # Esperar a que esté listo
            print("⏳ Esperando a que esté listo...")
            cmd = [
                "oc", "rollout", "status",
                f"-n{self.namespace}",
                "deployment/microservicio",
                "--timeout=5m"
            ]
            self.run_command(cmd)
    
    def check_database(self):
        """Verificar conexión a base de datos"""
        print(f"\n🗄️  Verificando base de datos...")
        print("=" * 50)
        
        # Obtener pod de PostgreSQL
        cmd = [
            "oc", "get", "pods",
            f"-n{self.namespace}",
            "-l", "app=postgres",
            "-o", "jsonpath={.items[0].metadata.name}"
        ]
        pod_name = self.run_command(cmd, capture_output=True)
        
        if pod_name:
            cmd = [
                "oc", "exec", "-it", pod_name,
                f"-n{self.namespace}",
                "--", "pg_isready", "-U", "usuario"
            ]
            self.run_command(cmd)
    
    def test_health(self):
        """Probar endpoint de health"""
        print(f"\n❤️  Probando health check...")
        print("=" * 50)
        
        # Obtener ruta
        cmd = [
            "oc", "get", "route", "microservicio",
            f"-n{self.namespace}",
            "-o", "jsonpath={.spec.host}"
        ]
        host = self.run_command(cmd, capture_output=True)
        
        if host:
            print(f"URL: https://{host}/health")
            import urllib.request
            try:
                response = urllib.request.urlopen(f"https://{host}/health", context=None)
                print(f"✓ Health check: OK (status {response.getcode()})")
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Gestor de despliegues en OpenShift"
    )
    
    parser.add_argument(
        "command",
        choices=[
            "status", "logs", "describe", "restart",
            "db-check", "health", "login"
        ],
        help="Comando a ejecutar"
    )
    
    parser.add_argument(
        "--follow", "-f",
        action="store_true",
        help="Seguir logs en tiempo real"
    )
    
    parser.add_argument(
        "--tail",
        type=int,
        default=50,
        help="Número de líneas de logs a mostrar"
    )
    
    parser.add_argument(
        "--pod",
        help="Nombre del pod (para describe)"
    )
    
    args = parser.parse_args()
    
    manager = OpenShiftManager()
    
    if args.command == "login":
        manager.login()
    elif args.command == "status":
        manager.login()
        manager.get_status()
    elif args.command == "logs":
        manager.login()
        manager.view_logs(follow=args.follow, tail=args.tail)
    elif args.command == "describe":
        manager.login()
        manager.describe_pod(args.pod)
    elif args.command == "restart":
        manager.login()
        manager.restart_deployment()
    elif args.command == "db-check":
        manager.login()
        manager.check_database()
    elif args.command == "health":
        manager.login()
        manager.test_health()


if __name__ == "__main__":
    main()
