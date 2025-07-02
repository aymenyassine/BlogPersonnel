# from itertools import count
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import get_user_model
# from django.views import View
# from django.contrib.auth.models import AnonymousUser
# from django.db.models import Count


# from support.models import Ticket
# from .models import Category, Post,Like,Notification
# from .forms import PostForm, CommentForm, SignalForm
# from django.contrib.auth.decorators import login_required

# # def home(request):
# #     posts = Post.objects.all().order_by('-created_at')
# #     if isinstance(request.user, AnonymousUser):
        
# #         notifications = []  
# #     else:
# #         notifications = Notification.objects.filter(user=request.user, is_read=False)
# #     return render(request, 'blog/home.html', {'posts': posts,'notifications': notifications})

# def home(request):
#     category_id = request.GET.get('category')
#     sort_by_likes = request.GET.get('sort') == 'likes'

#     posts = Post.objects.all()

#     if category_id:
#         posts = posts.filter(category__id=category_id)

#     if sort_by_likes:
#         posts = posts.annotate(num_likes=Count('likes')).order_by('-num_likes')

#     categories = Category.objects.all()
#     if isinstance(request.user, AnonymousUser):
        
#         notifications = []  
#     else:
#         notifications = Notification.objects.filter(user=request.user, is_read=False)
#     return render(request, 'blog/home.html', {
#         'posts': posts,
#         'categories': categories,'notifications': notifications
#     })

# @login_required
# def post_create(request):
#     form = PostForm(request.POST or None, request.FILES or None)
#     if isinstance(request.user, AnonymousUser):
        
#         notifications = []  
#     else:
#         notifications = Notification.objects.filter(user=request.user, is_read=False)
#     if form.is_valid():
#         post = form.save(commit=False)
#         post.author = request.user
#         post.save()
#         return redirect('home')
#     return render(request, 'blog/post_form.html', {'form': form,'notifications': notifications})

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if isinstance(request.user, AnonymousUser):
        
#         notifications = []  
#     else:
#         notifications = Notification.objects.filter(user=request.user, is_read=False)
#     comments = post.comments.all()
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             Notification.objects.create(
#             user=post.author,
#             post = post,
#             message=f"{request.user.username} a commenter votre post : {post.title}"
#         )

#             return redirect('post_detail', pk=pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form,'notifications': notifications})

# @login_required
# def like_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
    
#     like = Like.objects.filter(post=post, user=request.user).first()
#     if like:
#         like.delete()
#     else:
#         Like.objects.create(post=post, user=request.user)
#         Notification.objects.create(
#             user=post.author,
#             post = post,
#             message=f"{request.user.username} a aimé votre post : {post.title}"
#         )
#     return redirect('post_detail', pk=pk)

# @login_required
# def signaler_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if isinstance(request.user, AnonymousUser):
        
#         notifications = []  
#     else:
#         notifications = Notification.objects.filter(user=request.user, is_read=False)
#     if request.method == 'POST':
#         form = SignalForm(request.POST)
#         if form.is_valid():
#             signal = form.save(commit=False)
#             signal.user = request.user
#             signal.post = post
#             signal.save()

#             # Créer un ticket automatiquement pour ce signalement
#             Ticket.objects.create(signalement=signal)

#             return redirect('home')
#     else:
#         form = SignalForm()

#     return render(request, 'blog/signal_post.html', {'form': form, 'post': post, 'notifications': notifications})


# class  Postmodifier(View):
#     def get(self ,request,id):
#         post = Post.objects.get(id=id)
#         if isinstance(request.user, AnonymousUser):
        
#             notifications = []  
#         else:
#             notifications = Notification.objects.filter(user=request.user, is_read=False)
#         form = PostForm(instance=post)
#         return render(request, 'blog/post_form.html', {'form': form,'notifications': notifications})
#     def post(self, request, id):
#         if isinstance(request.user, AnonymousUser):
        
#             notifications = []  
#         else:
#             notifications = Notification.objects.filter(user=request.user, is_read=False)
#         post = Post.objects.get(id=id)
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         return render(request, 'blog/post_form.html', {'form': form,'notifications': notifications})

  
# class PostSupprimer(View):
#     def get(self, request, id):
#         post = Post.objects.get(id=id)
#         post.delete()
#         return redirect('home')
    

# def profile_view(request, user_id=None):
#     if isinstance(request.user, AnonymousUser):
        
#         notifications = []  
#     else:
#         notifications = Notification.objects.filter(user=request.user, is_read=False)
#     if user_id:
#         user = get_object_or_404(get_user_model(), id=user_id)
#     else:
#         user = request.user

#     posts = Post.objects.filter(author=user).order_by('-created_at')
    
#     return render(request, 'blog/profile.html', {'user_profile': user, 'posts': posts,'notifications': notifications})


# @login_required
# def mark_notifications_as_read(request):
#     if isinstance(request.user, AnonymousUser):
        
#         notifications = []  
#     else:
#         notifications = Notification.objects.filter(user=request.user, is_read=False)

#     for notification in notifications:
#         notification.is_read = True
#         notification.save()
#         if notification.post:
#             return redirect('post_detail', pk=notification.post.pk)    
#     return redirect('profile_view')
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment, Like, Notification, Category, Signaler
from .serializers import PostSerializer, CommentSerializer, NotificationSerializer, CategorySerializer, SignalerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Like
from .serializers import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count
from support.serializers import TicketSerializer
from support.models import Ticket
from rest_framework.permissions import IsAuthenticated

class PostList(APIView):
    """
    Afficher une liste de tous les posts (triés par date la plus récente)
    ou en créer un nouveau.
    """

    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        search_query = request.query_params.get('search', '')
        
        if search_query:
            posts = Post.objects.filter(title__icontains=search_query).order_by('-created_at')
        else:
            posts = Post.objects.all().order_by('-created_at')
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("Received data:", request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Utilise l'utilisateur authentifié comme auteur
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PostDetail(APIView):
    """
    Afficher un post spécifique et permettre de le mettre à jour ou de le supprimer.
    """

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.views += 1  # 👈 Incrémentation des vues
            post.save(update_fields=['views'])  # 👈 On enregistre uniquement le champ views
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class PostLike(APIView):
    """
    Permet à un utilisateur d'aimer un post et récupérer le statut
    """
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        like_count = post.likes.count()
        user_has_liked = post.likes.filter(user=request.user).exists()
        return Response({
            'liked': user_has_liked,
            'like_count': like_count
        })

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()
            return Response({
                'status': 'unliked',
                'like_count': post.likes.count()  # Retourne le nouveau compte
            })
        
        return Response({
            'status': 'liked',
            'like_count': post.likes.count()  # Retourne le nouveau compte
        })


class CommentList(APIView):
    """
    Afficher la liste des commentaires pour un post spécifique.
    """
    def get(self, request, post_pk):
        comments = Comment.objects.filter(post__id=post_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_pk):
        post = Post.objects.get(pk=post_pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationList(APIView):
    """
    Liste les notifications pour l'utilisateur.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Marquer les notifications comme lues
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'notifications marked as read'})

class CategoryList(APIView):
    """
    Liste des catégories disponibles.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
class CategoryType(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request,pk):
        categories = Category.objects.get(pk=pk)
        serializer = CategorySerializer(categories, many=False)
        return Response(serializer.data)
    
class SignalerList(APIView):
    """
    Permet de signaler un post et crée automatiquement un ticket associé.
    """
    permission_classes = [IsAuthenticated]  # Seuls les utilisateurs authentifiés peuvent signaler

    def post(self, request):
        # Création du signalement
        signaler_serializer = SignalerSerializer(data=request.data, context={'request': request})
        if not signaler_serializer.is_valid():
            return Response(signaler_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        signalement = signaler_serializer.save(user=request.user)
        
        # Création automatique du ticket associé
        try:
            ticket = Ticket.objects.create(
                signalement=signalement,
                status='En_cours'  # Statut par défaut
            )
            
            # Vous pourriez aussi assigner automatiquement un agent support ici si nécessaire
            # ticket.support_agent = assign_agent()
            # ticket.save()
            
            ticket_serializer = TicketSerializer(ticket)
            
            response_data = {
                'signalement': signaler_serializer.data,
                'ticket': ticket_serializer.data,
                'message': 'Signalement créé avec succès et ticket généré'
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # En cas d'échec de création du ticket, supprimer le signalement créé
            signalement.delete()
            return Response(
                {'error': f"Erreur lors de la création du ticket: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """Liste des signalements (peut être modifié selon vos besoins)"""
        signalers = Signaler.objects.all()
        serializer = SignalerSerializer(signalers, many=True)
        return Response(serializer.data)
    

class TopTrendsView(APIView):
    def get(self, request):
        today = timezone.now().date()
        top_posts = Post.objects.filter(created_at__date=today).order_by('-views')[:5]
        data = [{"id": post.id, "title": post.title} for post in top_posts]
        return Response(data, status=status.HTTP_200_OK)


class TopicsForYouView(APIView):
    def get(self, request):
        categories = Category.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:6]
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
