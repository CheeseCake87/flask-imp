from . import db

sql_do = db.session

# Permissions are used to disable certain features
class FlPermissions(db.Model):
    __tablename__ = "fl_permissions"
    permissions_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text)
    name = db.Column(db.Text)


class FlPermissionsMembership(db.Model):
    __tablename__ = "fl_perissions_membership"
    permission_membership_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    permissions_id = db.Column(db.Integer)

# A user in a Clan is unable to see anything from another Clan
class FlClan(db.Model):
    __tablename__ = "fl_clan"
    clan_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


class FlClanMembership(db.Model):
    __tablename__ = "fl_clan_membership"
    clan_membership_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    clan_id = db.Column(db.Integer)

# A user in a Teams are able to scope data
class FlTeam(db.Model):
    __tablename__ = "fl_team"
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


class FlTeamMembership(db.Model):
    __tablename__ = "fl_team_membership"
    team_membership_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    team_id = db.Column(db.Integer)
